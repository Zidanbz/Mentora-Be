import os
import google.generativeai as genai
from dotenv import load_dotenv

# Muat environment variables dari file .env
load_dotenv()

# Konfigurasi API key
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Inisialisasi model
# 'gemini-1.5-pro-latest' adalah model yang sangat kuat. 
# Anda juga bisa pakai 'gemini-1.5-flash-latest' untuk respon lebih cepat & lebih murah.
model = genai.GenerativeModel('gemini-1.5-flash-latest') 

# Kirim pertanyaan ke Gemini
prompt = "Jelaskan apa itu 'Customer Lifetime Value' dengan bahasa yang mudah dimengerti oleh pemilik UMKM."
response = model.generate_content(prompt)

# Tampilkan jawaban dari AI
print(response.text)