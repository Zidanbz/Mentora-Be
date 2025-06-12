# dashboard/chatbot_tools.py
from .models import Product

def get_product_count() -> int:
    """
    Mengembalikan jumlah total produk yang terdaftar di database.
    """
    print("LOG: Menjalankan fungsi get_product_count...")
    count = Product.objects.count()
    return count

def get_product_list() -> str:
    """
    Mengembalikan daftar nama semua produk yang ada, dipisahkan dengan koma.
    """
    print("LOG: Menjalankan fungsi get_product_list...")
    products = Product.objects.all()
    if not products:
        return "Tidak ada produk yang ditemukan."
    
    # Gabungkan nama produk menjadi satu string
    product_names = ", ".join([p.name for p in products])
    return product_names

def get_most_expensive_product() -> str:
    """
    Menemukan dan mengembalikan nama produk dengan harga tertinggi.
    """
    print("LOG: Menjalankan fungsi get_most_expensive_product...")
    product = Product.objects.order_by('-price').first()
    if product:
        return f"Produk termahal adalah {product.name} dengan harga Rp {product.price:,.0f}."
    return "Tidak ada produk di database."

# Anda bisa menambahkan lebih banyak 'tools' di sini di masa depan!