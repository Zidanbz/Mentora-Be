# dashboard/chatbot_tools.py
from .models import Product
from accounts.models import Company
from .models import Product, Sale 
from django.utils import timezone
from datetime import timedelta

class CompanyAwareTools:
    """
    Sebuah 'kotak perkakas' yang dibuat khusus untuk satu perusahaan.
    Semua fungsi (metode) di dalamnya secara otomatis terhubung ke perusahaan tersebut.
    """
    def __init__(self, company: Company):
        # Saat 'kotak' ini dibuat, kita simpan informasi perusahaannya.
        self.company = company

    def get_product_count(self) -> int:
        """
        Mengembalikan jumlah total produk untuk perusahaan ini.
        """
        print(f"LOG: Menjalankan get_product_count untuk {self.company.name}...")
        return Product.objects.filter(company=self.company).count()

    def get_product_list(self) -> str:
        """
        Mengembalikan daftar nama semua produk untuk perusahaan ini, dipisahkan koma.
        """
        print(f"LOG: Menjalankan get_product_list untuk {self.company.name}...")
        products = Product.objects.filter(company=self.company)
        if not products:
            return "Tidak ada produk yang ditemukan untuk perusahaan Anda."
        return ", ".join([p.name for p in products])

    def get_most_expensive_product(self) -> str:
        """
        Menemukan dan mengembalikan nama produk termahal untuk perusahaan ini.
        """
        print(f"LOG: Menjalankan get_most_expensive_product untuk {self.company.name}...")
        product = Product.objects.filter(company=self.company).order_by('-price').first()
        if product:
            return f"Produk termahal Anda adalah {product.name} dengan harga Rp {product.price:,.0f}."
        return "Tidak ada produk di database perusahaan Anda."

    def analyze_weekly_sales_trend(self) -> str:
        """
        Menganalisis total pendapatan penjualan dari 7 hari terakhir dan membandingkannya
        dengan 7 hari sebelumnya untuk memberikan analisis tren.
        """
        print(f"LOG: Menjalankan analyze_weekly_sales_trend untuk {self.company.name}...")
        now = timezone.now()
        
        # Hitung pendapatan 7 hari terakhir
        start_current_week = now - timedelta(days=7)
        sales_current_week = Sale.objects.filter(company=self.company, sale_date__gte=start_current_week)
        revenue_current_week = sum(item.product.price * item.quantity for item in sales_current_week)

        # Hitung pendapatan 7 hari sebelumnya
        start_previous_week = start_current_week - timedelta(days=7)
        sales_previous_week = Sale.objects.filter(company=self.company, sale_date__gte=start_previous_week, sale_date__lt=start_current_week)
        revenue_previous_week = sum(item.product.price * item.quantity for item in sales_previous_week)

        # Analisis dan buat respons
        if revenue_current_week == 0 and revenue_previous_week == 0:
            return "Tidak ada data penjualan yang tercatat dalam 14 hari terakhir untuk dianalisis."
        
        if revenue_previous_week == 0:
             return f"Penjualan minggu ini dimulai dengan baik dengan total pendapatan Rp {revenue_current_week:,.0f}."

        percentage_change = ((revenue_current_week - revenue_previous_week) / revenue_previous_week) * 100
        
        if percentage_change > 0:
            trend = f"naik sebesar {percentage_change:.2f}%"
        elif percentage_change < 0:
            trend = f"turun sebesar {abs(percentage_change):.2f}%"
        else:
            trend = "stabil"
            
        return (f"Analisis tren penjualan mingguan: Pendapatan 7 hari terakhir adalah Rp {revenue_current_week:,.0f}. "
                f"Ini {trend} dibandingkan dengan 7 hari sebelumnya (Rp {revenue_previous_week:,.0f}).")
