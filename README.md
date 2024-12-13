# Culture Connect Machine Learning API

This is a FastAPI backend API for provide a Machine Learning-based on mobile application. 

Technologies Used:
- python
- docker
- fastapi ( backend framework )

## How To Use

1. **Kloning Repositori**
   ```bash
   
   https://github.com/CultureConnect2024/Backend-API.git
   
   cd Backend-API
2. **Create Virtual ENV**
   ```bash
   python -m venv venv

3. **Activate the virtual env (gitbash)**
   ```bash
   source venv/Scripts/activate
   
4. **Activate the virtual env (cmd)**
   ```bash
   venv/Scripts/activate.bat

5. **Install the requirements**
   ```bash
   pip install -r requirements.txt

5. **Run Project**
   ```bash
   fastapi dev main.py


# API Documentation

This API allows for user registration, login, logout, and health check, as well as testing the database connection.

## Endpoints

### 1. Predict Endpoint
#### `POST /predict_mood`
Predict Mood Data From Text Input.

**Response:**
- **200 OK** - If the predict succesfully.
- **404 Not Found** - If the api image or data not found.
- **404 Not Found** - If the text failed to be predicted.

  **Request Body:**
  ```bash
  {
    "text" : "<text input from users>"
  }
   ```

  Response:
  ```bash
  {
      "Predicted Mood": "< top mood > ",
      "Confidence Scores": {
          "Sadness": "<score>",
          "Joy": "<score>",
          "Love": "<score>",
          "Anger": "<score>",
          "Fear": "<score>",
          "Surprise": "<score>"
      },
      "Cafe Recommendation": {
          "Page_URL": "<google maps url",
          "Title": "<cafe title>",
          "Rating": "<rating cafe>",
          "Reviews": "<cafe reviews count>",
          "Address": "<cafe address>",
          "Phone_Number": "<cafe phone number's",
          "Price": "<price range>",
          "Category": "<place category>",
          "Jadwal": "<cafe-data-schedule>",
          "Plus_code": "<plus code>",
          "image": "<image url>",
          "Opsi_Layanan": "<cafe service option>",
          "Penawaran": "<additional service from cafe>",
          "Pilihan_Makanan": "Type Of Food",
          "Fasilitas": "Cafe facilities",
          "Suasana": "cafe environment",
          "Tipe_pengunjung": "Type Of Guest",
          "Perencanaan": "Planing",
          "Pembayaran": "<type of order payments>",
          "anak_anak": "<children only or not",
          "Parkir": "<Parking Rules"
      },
      "Quote": "<Quote Moods",
      "Today's word for you": "<Input text from users>""
  }



 **Example Request Body:**
  ```bash
   {
    "text": "Today has been such a wonderful day. I woke up early, went for a run, had a great breakfast, and then spent time with my friends. We laughed,
    talked about our dreams, and shared some amazing stories. I'm feeling so energized and excited for everything that's coming"
  }
   ```

**Example Response**
  ```bash
   {
    "Predicted Mood": "Joy",
    "Confidence Scores": {
        "Sadness": 0.71,
        "Joy": 98.11,
        "Love": 1.1,
        "Anger": 0.04,
        "Fear": 0.01,
        "Surprise": 0.03
    },
    "Cafe Recommendation": {
        "Page_URL": "https://www.google.com/maps/place/Cafe+banyumili+solo/@-7.5681003,110.8079553,17z/data=!3m1!4b1!4m6!3m5!1s0x2e7a17dbccad2e09:0xcb46d99939752dcf!8m2!3d-7.5681003!4d110.8105302!16s%2Fg%2F11j4lqvcbd?entry=ttu&g_ep=EgoyMDI0MTEyNC4xIKXMDSoJLDEwMjExMjM0SAFQAw%3D%3D",
        "Title": "Cafe banyumili solo",
        "Rating": "4,6",
        "Reviews": 10,
        "Address": "\nJl. Bhayangkara No.81, Sriwedari, Kec. Laweyan, Kota Surakarta, Jawa Tengah 57141",
        "Phone_Number": "Tidak tersedia",
        "Price": "Rp 25–50 rb",
        "Category": "Kafe",
        "Jadwal": "Senin 10.00–00.00\nSelasa 10.00–00.00\nRabu 10.00–00.00\nKamis 10.00–00.00\nJumat 10.00–00.00\nSabtu 10.00–00.00\nMinggu 10.00–22.00",
        "Plus_code": "CRJ6+Q6 Sriwedari, Kota Surakarta, Jawa Tengah",
        "image": "https://lh5.googleusercontent.com/p/AF1QipMJvWPnh4o0XQM12nKi07PU91D3S3A2JLAjI3bf=w408-h509-k-no",
        "Opsi_Layanan": "Tempat duduk di area terbuka\nBawa pulang\nMakan di tempat",
        "Penawaran": "Alkohol\nKopi",
        "Pilihan_Makanan": "Makan siang\nMakan malam\nHidangan penutup",
        "Fasilitas": "Memiliki bar\nToilet",
        "Suasana": "Nyaman\nSantai",
        "Tipe_pengunjung": "Berkelompok",
        "Perencanaan": "Menerima reservasi",
        "Pembayaran": "Hanya Tunai",
        "anak_anak": "Cocok untuk anak-anak",
        "Parkir": "Tempat parkir berbayar"
    },
    "Quote": "\"Joy is the simplest form of gratitude.\" - Karl Barth",
    "Today's word for you": "\"Today has been such a wonderful day. I woke up early, went for a run, had a great breakfast, and then spent time with my friends. We laughed, talked about our dreams, and shared some amazing stories. I'm feeling so energized and excited for everything that's coming\""
}
   ```

### 2. Fetch Cafe Data Endpoint
#### `GET /get_all_cafe_data`
Get All Data Cafe Recomendations.
**Response:**
- **200 OK** - If get data succesffully.
- **404 Not Found** - If the  data not found.
  ```bash
   {
       "Cafe Data": [
           {
               "Page_URL": "<google maps url",
             "Title": "<cafe title>",
             "Rating": "<rating cafe>",
             "Reviews": "<cafe reviews count>",
             "Address": "<cafe address>",
             "Phone_Number": "<cafe phone number's",
             "Price": "<price range>",
             "Category": "<place category>",
             "Jadwal": "<cafe-data-schedule>",
             "Plus_code": "<plus code>",
             "image": "<image url>",
             "Opsi_Layanan": "<cafe service option>",
             "Penawaran": "<additional service from cafe>",
             "Pilihan_Makanan": "Type Of Food",
             "Fasilitas": "Cafe facilities",
             "Suasana": "cafe environment",
             "Tipe_pengunjung": "Type Of Guest",
             "Perencanaan": "Planing",
             "Pembayaran": "<type of order payments>",
             "anak_anak": "<children only or not",
             "Parkir": "<Parking Rules"
         },
         "Quote": "<Quote Moods",
         "Today's word for you": "<Input text from users>""
           },
   
   .....
   
     ]
   }
 ```

       


