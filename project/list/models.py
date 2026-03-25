from django.db import models
from django.contrib.auth.models import User

class Store(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Magazin nomi")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Magazin"
        verbose_name_plural = "Magazinlar"

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Foydalanuvchi", default=1)
    date = models.DateField(verbose_name="Sana")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name="Magazin")
    length = models.FloatField(help_text="Uzunligi (m)", verbose_name="Uzunlik", default=0)
    width = models.FloatField(help_text="Eni (m)", verbose_name="En", default=0)
    thickness = models.FloatField(help_text="Qalinligi (m)", verbose_name="Qalinlik", default=0)
    density = models.FloatField(help_text="Zichligi (kg/m³)", verbose_name="Zichlik", default=0)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, help_text="Kg uchun narx (so'm)", verbose_name="Kg uchun narx", default=0)
    quantity = models.IntegerField(verbose_name="Soni", default=0)

    @property
    def mass(self):
        return self.length * self.width * self.thickness * self.density

    @property
    def sheet_price(self):
        return self.mass * float(self.price_per_kg)

    @property
    def total_cost(self):
        return self.quantity * self.sheet_price

    def __str__(self):
        return f"Xarid: {self.store.name} - {self.length}x{self.width}x{self.thickness} - {self.quantity} dona"

    class Meta:
        verbose_name = "Xarid"
        verbose_name_plural = "Xaridlar"

class History(models.Model):
    ACTION_CHOICES = [
        ('create', 'Yaratish'),
        ('update', 'Yangilash'),
        ('delete', "O'chirish"),
        ('login', 'Tizimga kirish'),
        ('logout', 'Tizimdan chiqish'),
    ]
    
    MODEL_CHOICES = [
        ('store', 'Magazin'),
        ('purchase', 'Xarid'),
        ('user', 'Foydalanuvchi'),
        ('auth', 'Avtorizatsiya'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Bajaruvchi")
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, verbose_name="Amal")
    model_type = models.CharField(max_length=10, choices=MODEL_CHOICES, verbose_name="Model turi")
    object_id = models.PositiveIntegerField(null=True, blank=True, verbose_name="Obekt ID")
    object_repr = models.CharField(max_length=200, verbose_name="Obekt nomi")
    description = models.TextField(verbose_name="Tavsif")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Vaqt")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP manzil")
    user_agent = models.TextField(null=True, blank=True, verbose_name="Brauzer ma'lumoti")

    class Meta:
        verbose_name = "Tarix"
        verbose_name_plural = "Tarix"
        ordering = ['-timestamp']

    def __str__(self):
        user_name = self.user.username if self.user else "Noma'lum"
        return f"{user_name} - {self.get_action_display()} - {self.object_repr}"
