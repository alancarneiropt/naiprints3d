from django import forms
from django.utils.text import slugify

from .models import Product


class FeaturedProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "category",
            "name",
            "slug",
            "short_description",
            "description",
            "image",
            "is_featured",
            "is_active",
            "order",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug", "").strip()
        name = self.cleaned_data.get("name", "").strip()
        return slug or slugify(name)
