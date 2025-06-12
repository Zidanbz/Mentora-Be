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