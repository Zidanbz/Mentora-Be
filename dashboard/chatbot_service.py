# dashboard/chatbot_service.py
import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from .chatbot_tools import CompanyAwareTools # <-- Import Class, bukan modul
from accounts.models import Company
from .models import ChatHistory # <-- 1. Import model ChatHistory

def run_chatbot_conversation(user_prompt: str, company: Company) -> str:
    """
    Menjalankan sesi percakapan menggunakan instance dari CompanyAwareTools.
    SEKARANG MENYERTAKAN RIWAYAT PERCAKAPAN UNTUK MEMBERIKAN KONTEKS.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)

    # 2. Ambil riwayat percakapan sebelumnya dari database
    # Ambil 5 percakapan terakhir (paling baru) untuk menjaga konteks tetap relevan.
    recent_conversations = ChatHistory.objects.filter(company=company)[:5]
    
    # Model ChatHistory sudah diurutkan dari terbaru, jadi kita balik urutannya
    # agar menjadi kronologis (dari yang terlama ke terbaru) untuk AI.
    past_conversations = reversed(recent_conversations)
    
    formatted_history = []
    for conv in past_conversations:
        formatted_history.append({'role': 'user', 'parts': [{'text': conv.prompt}]})
        formatted_history.append({'role': 'model', 'parts': [{'text': conv.response}]})

    # 3. Buat sebuah instance 'kotak perkakas' khusus untuk perusahaan ini
    tool_instance = CompanyAwareTools(company=company)

    # 4. Berikan metode-metode dari instance tersebut sebagai alat ke Gemini
    model = genai.GenerativeModel(
        model_name='gemini-1.5-pro-latest',
        tools=[
            tool_instance.get_product_count,
            tool_instance.get_product_list,
            tool_instance.get_most_expensive_product,
            tool_instance.analyze_weekly_sales_trend,
        ],
        safety_settings={
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
    )

    # 5. Mulai chat DENGAN RIWAYAT PERCAKAPAN sebagai konteks awal
    chat = model.start_chat(history=formatted_history, enable_automatic_function_calling=True)

    try:
        response = chat.send_message(user_prompt)
        return response.text
    except Exception as e:
        print(f"DEBUG: Terjadi error internal saat menghubungi Gemini API: {e}")
        return "Maaf, terjadi kesalahan pada sistem AI kami. Silakan cek terminal Django untuk detail error."
