import tensorflow as tf
import json
import pandas as pd
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import storage
import numpy as np
import math
import os
from dotenv import load_dotenv
import io

# Memuat env
load_dotenv()


app = FastAPI()

# Fungsi untuk memeriksa nilai yang tidak valid 
def filter_invalid_values(data):
    if isinstance(data, float) and not math.isfinite(data):
        return None  # Ganti dengan nilai yang valid atau hilangkan
    if isinstance(data, dict):
        return {k: filter_invalid_values(v) for k, v in data.items()}
    if isinstance(data, list):
        return [filter_invalid_values(v) for v in data]
    return data

# Fungsi untuk mengonversi numpy.float32 menjadi float
def convert_numpy_floats(data):
    if isinstance(data, np.float32):
        return float(data)
    elif isinstance(data, dict):
        return {k: convert_numpy_floats(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_numpy_floats(v) for v in data]
    return data

# Path di Google Cloud Storage untuk model dan tokenizer
BUCKET_NAME = os.getenv("BUCKET_NAME2")
MODEL_PATH = "Model-Final"
TOKENIZER_PATH = "Model-Final/assets/tokenizer.json"

# Fungsi untuk mendapatkan klien Google Cloud Storage
def get_storage_client():
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not cred_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")
    client = storage.Client.from_service_account_json(cred_path)
    return client

# Fungsi untuk mengunduh file dari Google Cloud Storage
def download_from_gcs(bucket_name, gcs_path):
    client = get_storage_client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(gcs_path)
    return blob.download_as_bytes()

# Memuat tokenizer dari GCS
try:
    tokenizer_bytes = download_from_gcs(BUCKET_NAME, TOKENIZER_PATH)
    tokenizer_json = tokenizer_bytes.decode("utf-8")
    tokenizer = tokenizer_from_json(tokenizer_json)
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error loading tokenizer: {str(e)}")


# Fungsi untuk mengunduh file CSV dari GCS
def download_csv_from_gcs(bucket_name, gcs_path):
    client = get_storage_client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(gcs_path)
    # Mengunduh sebagai byte stream
    csv_data = blob.download_as_bytes()
    # Membaca byte stream menjadi DataFrame
    return pd.read_csv(io.BytesIO(csv_data))

# Memuat data cafe untuk setiap mood
try:
    cafe_data = {
        'Anger': download_csv_from_gcs('ml-caffe-data', 'anger_caffe.csv'),
        'Joy': download_csv_from_gcs('ml-caffe-data', 'joy_caffe.csv'),
        'Sadness': download_csv_from_gcs('ml-caffe-data', 'sadness_caffe.csv'),
        'Love': download_csv_from_gcs('ml-caffe-data', 'love_caffe.csv'),
        'Fear': download_csv_from_gcs('ml-caffe-data', 'fear_caffe.csv'),
        'Surprise': download_csv_from_gcs('ml-caffe-data', 'surprise_caffe.csv'),
    }
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error loading cafe data: {str(e)}")


# Load quotes data
try:
    quotes_df = download_csv_from_gcs('ml-caffe-data', 'Quotes_Mood.csv')
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error loading quotes data: {str(e)}")


# Memuat model dari GCS
try:
    temp_model_dir = "./temp_model_dir"
    os.makedirs(temp_model_dir, exist_ok=True)

    # Unduh model
    model_bytes = download_from_gcs(BUCKET_NAME, MODEL_PATH + "/saved_model.pb")
    variables_bytes = {
        "data": download_from_gcs(BUCKET_NAME, MODEL_PATH + "/variables/variables.data-00000-of-00001"),
        "index": download_from_gcs(BUCKET_NAME, MODEL_PATH + "/variables/variables.index"),
    }

    # Simpan file sementara
    with open(f"{temp_model_dir}/saved_model.pb", "wb") as f:
        f.write(model_bytes)
    os.makedirs(f"{temp_model_dir}/variables", exist_ok=True)
    with open(f"{temp_model_dir}/variables/variables.data-00000-of-00001", "wb") as f:
        f.write(variables_bytes["data"])
    with open(f"{temp_model_dir}/variables/variables.index", "wb") as f:
        f.write(variables_bytes["index"])

    # Muat model dari direktori sementara
    model = tf.saved_model.load(temp_model_dir)
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error loading model: {str(e)}")

# Define input data model untuk FastAPI
class TextRequest(BaseModel):
    text: str

# Fungsi prediksi mood
def predict_mood(text: str):
    try:
        # Tokenisasi input teks
        sequences = tokenizer.texts_to_sequences([text])
        padded_sequences = tf.keras.preprocessing.sequence.pad_sequences(sequences, padding='post', maxlen=150)
        input_tensor = tf.convert_to_tensor(padded_sequences, dtype=tf.float32)

        # Tambahkan dimensi ekstra jika model memerlukan input 4D
        if len(input_tensor.shape) == 3:
            input_tensor = tf.expand_dims(input_tensor, axis=-1)

        # Ambil fungsi inferensi dari model
        infer = model.signatures["serving_default"]

        # Lakukan prediksi
        predictions = infer(input_tensor)

        # Ambil skor kepercayaan (asumsikan output ada di 'output_0')
        confidence_scores = predictions['output_0'].numpy()[0]

        # Daftar mood
        moods = ['Sadness', 'Joy', 'Love', 'Anger', 'Fear', 'Surprise']

        # Pemetaan skor mood
        mood_scores = {mood: confidence_scores[i] * 100 for i, mood in enumerate(moods)}

        # Debugging untuk mood_scores
        print("Mood Scores:", mood_scores)

        # Memastikan tidak ada nilai NaN atau Infinity
        mood_scores = {mood: score if np.isfinite(score) else None for mood, score in mood_scores.items()}

        # Cek jika ada skor None dan batalkan prediksi jika ditemukan
        if any(v is None for v in mood_scores.values()):
            raise ValueError("Mood scores contain invalid values (None)")

        # Menentukan mood dengan skor tertinggi
        predicted_mood = max(mood_scores, key=lambda k: mood_scores[k] if mood_scores[k] is not None else -1)

        return predicted_mood, mood_scores

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")

# Fungsi untuk mendapatkan rekomendasi cafe berdasarkan mood
def get_cafe_recommendation(mood: str, num_recommendations: int = 3):
    cafes = cafe_data.get(mood)
    if cafes is not None and not cafes.empty:
        return cafes.sample(n=num_recommendations).to_dict(orient="records")  # Mengembalikan data dalam bentuk list of dicts
    else:
        return {"message": f"No cafe data available for mood: {mood}"}

# Fungsi untuk mendapatkan seluruh data cafe
def get_all_cafe_data():
    all_cafes = []
    for mood in cafe_data.keys():
        cafes = cafe_data.get(mood)
        if cafes is not None and not cafes.empty:
            cafes_data = cafes.to_dict(orient="records")
            all_cafes.extend(cafes_data)
    return all_cafes

# Fungsi untuk mendapatkan quote berdasarkan mood
def get_quote(mood: str):
    quotes = quotes_df[quotes_df['Mood'] == mood]
    if not quotes.empty:
        return quotes.sample(1)['Quotes'].values[0]
    else:
        return "No quote available for this mood."

# Define the POST endpoint for mood prediction
@app.post("/predict_mood")
async def predict_mood_endpoint(request: TextRequest):
    text = request.text

    # Validasi input
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")

    try:
        predicted_mood, mood_scores = predict_mood(text)
        cafe_recommendation = get_cafe_recommendation(predicted_mood)
        quote = get_quote(predicted_mood)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    # Respons dengan mood, skor kepercayaan, rekomendasi cafe, dan quote
    response = {
        "Predicted Mood": predicted_mood,
        "Confidence Scores": convert_numpy_floats(mood_scores),
        "Cafe Recommendation": cafe_recommendation,
        "Quote": quote,
    }

    # Pastikan data dalam response valid dan aman untuk JSON
    response = filter_invalid_values(response)

    return response

# Endpoint untuk mendapatkan seluruh data cafe
@app.get("/get_all_cafe_data")
async def get_all_cafe_data_endpoint():
    try:
        cafes = get_all_cafe_data()
        
        # Filter invalid values
        cafes = [filter_invalid_values(cafe) for cafe in cafes]
        
        return {"Cafe Data": cafes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve cafe data: {str(e)}")