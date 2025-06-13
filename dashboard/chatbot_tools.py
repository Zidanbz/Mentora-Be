# dashboard/chatbot_tools.py
from .models import Product
from accounts.models import Company

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
