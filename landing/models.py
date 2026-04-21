from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=40, default="fa-cube")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    category = models.ForeignKey(Category, related_name="products", on_delete=models.PROTECT)
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=150, unique=True)
    short_description = models.CharField(max_length=220)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="products/", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_featured = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.name


class GalleryItem(TimeStampedModel):
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to="gallery/", blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Item de Galeria"
        verbose_name_plural = "Galeria"

    def __str__(self):
        return self.title


class SocialLink(TimeStampedModel):
    PLATFORM_CHOICES = [
        ("instagram", "Instagram"),
        ("facebook", "Facebook"),
        ("tiktok", "TikTok"),
        ("whatsapp", "WhatsApp"),
        ("email", "Email"),
        ("youtube", "YouTube"),
    ]

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, unique=True)
    label = models.CharField(max_length=80)
    url = models.URLField(max_length=300)
    icon = models.CharField(max_length=40, default="fa-link")
    is_primary_cta = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "platform"]
        verbose_name = "Rede Social / Contacto"
        verbose_name_plural = "Redes Sociais / Contactos"

    def __str__(self):
        return self.label
