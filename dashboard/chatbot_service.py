# dashboard/chatbot_service.py
import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from . import chatbot_tools # Import "alat" yang sudah kita buat
from google.generativeai.types import HarmCategory, HarmBlockThreshold

def run_chatbot_conversation(user_prompt: str) -> str:
    """
    Menjalankan sesi percakapan dengan Gemini dan menggunakan function calling.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)

    # Inisialisasi model dengan tools yang kita definisikan
    model = genai.GenerativeModel(
        model_name='gemini-1.5-pro-latest',
            tools=[
        chatbot_tools.get_product_count,
        chatbot_tools.get_product_list,
        chatbot_tools.get_most_expensive_product,
    ], # tools Anda tetap di sini
        safety_settings={
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
    )

    # Mulai sesi chat
    chat = model.start_chat(enable_automatic_function_calling=True)

    try:
        # Kirim prompt dari user ke model
        response = chat.send_message(user_prompt)
        
        # Kembalikan teks jawaban akhir dari model
        return response.text
    except Exception as e:
        # UBAH BAGIAN INI UNTUK DEBUGGING
        print("="*50)
        print(f"DEBUG: Terjadi error internal saat menghubungi Gemini API.")
        print(f"ERROR ASLI: {e}")
        print("="*50)
        return "Maaf, terjadi kesalahan pada sistem AI kami. Silakan cek terminal Django untuk detail error."