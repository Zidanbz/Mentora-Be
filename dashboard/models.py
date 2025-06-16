# dashboard/models.py

from django.db import models
# Hapus 'from django.contrib.auth.models import User' jika tidak digunakan lagi di sini

class Product(models.Model):
    # UBAH BARIS INI
    company = models.ForeignKey('accounts.Company', on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.company.name})"
    
    # === TAMBAHKAN MODEL BARU DI BAWAH INI ===
class ChatHistory(models.Model):
    company = models.ForeignKey('accounts.Company', on_delete=models.CASCADE)
    prompt = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat for {self.company.name} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        # Mengurutkan riwayat chat dari yang terbaru ke terlama
        ordering = ['-created_at']
        verbose_name_plural = "Chat Histories"

class Sale(models.Model):
    company = models.ForeignKey('accounts.Company', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for {self.company.name}"
