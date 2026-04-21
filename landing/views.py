from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
import os

from .forms import FeaturedProductForm
from .models import Category, GalleryItem, Product, SocialLink


def _fallback_categories():
    return [
        {"name": "Decoracao", "icon": "fa-wand-magic-sparkles"},
        {"name": "Organizacao", "icon": "fa-box-open"},
        {"name": "Suportes", "icon": "fa-mobile-screen"},
        {"name": "Personalizados", "icon": "fa-pen-ruler"},
        {"name": "Brindes", "icon": "fa-gift"},
        {"name": "Acessorios", "icon": "fa-puzzle-piece"},
        {"name": "Pecas por encomenda", "icon": "fa-gears"},
    ]


def _fallback_products():
    return [
        {
            "name": "Organizador de Secretaria Modular",
            "short_description": "Pecas modulares para manter o teu espaco de trabalho funcional e elegante.",
            "image_url": "https://images.unsplash.com/photo-1581094271901-8022df4466f9?auto=format&fit=crop&w=800&q=80",
        },
        {
            "name": "Suporte de Telemovel Ergonomico",
            "short_description": "Suporte resistente com angulo de visualizacao ideal para trabalho e videochamadas.",
            "image_url": "https://images.unsplash.com/photo-1611605698335-8b1569810432?auto=format&fit=crop&w=800&q=80",
        },
        {
            "name": "Luminaria Geometrica Decorativa",
            "short_description": "Design moderno para decorar ambientes com personalidade e estilo.",
            "image_url": "https://images.unsplash.com/photo-1519710164239-da123dc03ef4?auto=format&fit=crop&w=800&q=80",
        },
    ]


def _fallback_gallery():
    return [
        {"title": "Mockup 3D 1", "image_url": "https://images.unsplash.com/photo-1630080644615-0b7f7f4f8f8a?auto=format&fit=crop&w=800&q=80"},
        {"title": "Mockup 3D 2", "image_url": "https://images.unsplash.com/photo-1581093458791-9f3c3900df7b?auto=format&fit=crop&w=800&q=80"},
        {"title": "Mockup 3D 3", "image_url": "https://images.unsplash.com/photo-1581093458791-9f3c3900df7b?auto=format&fit=crop&w=500&q=80"},
        {"title": "Mockup 3D 4", "image_url": "https://images.unsplash.com/photo-1580982334325-78e4fdc97f5d?auto=format&fit=crop&w=800&q=80"},
    ]


def _fallback_social_links():
    return [
        {"label": "WhatsApp", "platform": "whatsapp", "url": "https://wa.me/351914073718", "icon": "fa-brands fa-whatsapp", "is_primary_cta": True},
        {"label": "Instagram", "platform": "instagram", "url": "https://www.instagram.com/naiprints3d_?igsh=dXdzZnUxMWo2b21j&utm_source=qr", "icon": "fa-brands fa-instagram"},
        {"label": "Email", "platform": "email", "url": "mailto:naiprints3d@gmail.com", "icon": "fa-regular fa-envelope"},
    ]


def home(request):
    categories = list(Category.objects.filter(is_active=True))
    products = list(Product.objects.filter(is_active=True, is_featured=True).select_related("category")[:8])
    gallery_items = list(GalleryItem.objects.filter(is_active=True).select_related("category")[:12])
    social_links = list(
        SocialLink.objects.filter(is_active=True).exclude(platform__in=["facebook", "tiktok"])
    )

    # Keep WhatsApp contact consistent even when legacy DB data exists.
    for social in social_links:
        if social.platform == "whatsapp":
            social.url = "https://wa.me/351914073718"

    context = {
        "site_name": "NaiPrints3D",
        "hero_title": "Transformamos ideias em produtos incriveis com impressao 3D",
        "hero_description": (
            "Criamos pecas decorativas, utilidades, brindes e solucoes personalizadas com foco em qualidade, "
            "criatividade e acabamento profissional."
        ),
        "categories": categories or _fallback_categories(),
        "products": products or _fallback_products(),
        "gallery_items": gallery_items or _fallback_gallery(),
        "social_links": social_links or _fallback_social_links(),
        "testimonials": [
            {
                "name": "Mariana Silva",
                "role": "Cliente particular",
                "avatar": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=200&q=80",
                "text": "Servico impecavel. O produto personalizado ficou ainda melhor do que imaginei.",
            },
            {
                "name": "Joao Ferreira",
                "role": "Empreendedor",
                "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=200&q=80",
                "text": "Qualidade top e entrega rapida. Voltarei a encomendar sem duvida.",
            },
            {
                "name": "Carla Mendes",
                "role": "Arquiteta de interiores",
                "avatar": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?auto=format&fit=crop&w=200&q=80",
                "text": "Pecas exclusivas, acabamento excelente e um atendimento super atencioso em cada detalhe.",
            },
        ],
        "how_it_works": [
            "Escolhe o produto",
            "Personaliza os detalhes",
            "Entra em contacto",
            "Recebe a tua encomenda",
        ],
        "seo": {
            "title": "NaiPrints3D | Produtos personalizados em impressao 3D",
            "description": "Descobre produtos modernos em impressao 3D: decoracao, organizacao, suportes e pecas personalizadas por encomenda.",
            "og_image": "https://images.unsplash.com/photo-1581092580497-e0d23cbdf1dc?auto=format&fit=crop&w=1200&q=80",
        },
    }
    return render(request, "landing/home.html", context)


def privacy_policy(request):
    return render(request, "landing/privacy_policy.html", {"site_name": "NaiPrints3D"})


def terms_conditions(request):
    return render(request, "landing/terms_conditions.html", {"site_name": "NaiPrints3D"})


def healthz(request):
    db_ok = os.path.isfile(settings.SQLITE_PATH)
    media_ok = os.path.isdir(settings.MEDIA_ROOT) and os.access(settings.MEDIA_ROOT, os.W_OK)
    status_code = 200 if db_ok and media_ok else 503
    return JsonResponse(
        {
            "status": "ok" if status_code == 200 else "error",
            "sqlite_path": settings.SQLITE_PATH,
            "db_file_exists": db_ok,
            "media_writable": media_ok,
        },
        status=status_code,
    )


class BackofficeLoginView(LoginView):
    template_name = "landing/backoffice/login.html"
    redirect_authenticated_user = True


@login_required
def backoffice_dashboard(request):
    products = Product.objects.select_related("category")
    return render(
        request,
        "landing/backoffice/dashboard.html",
        {"products": products},
    )


@login_required
def backoffice_product_create(request):
    if request.method == "POST":
        form = FeaturedProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto criado com sucesso.")
            return redirect("landing:backoffice_dashboard")
    else:
        form = FeaturedProductForm(initial={"is_featured": True, "is_active": True})
    return render(
        request,
        "landing/backoffice/product_form.html",
        {"form": form, "page_title": "Novo produto em destaque"},
    )


@login_required
def backoffice_product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = FeaturedProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto atualizado com sucesso.")
            return redirect("landing:backoffice_dashboard")
    else:
        form = FeaturedProductForm(instance=product)
    return render(
        request,
        "landing/backoffice/product_form.html",
        {"form": form, "page_title": f"Editar: {product.name}"},
    )


@login_required
def backoffice_product_toggle_featured(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.is_featured = not product.is_featured
    product.save(update_fields=["is_featured", "updated_at"])
    messages.success(request, "Destaque do produto atualizado.")
    return redirect("landing:backoffice_dashboard")


@login_required
def backoffice_product_delete(request, product_id):
    if request.method != "POST":
        return redirect("landing:backoffice_dashboard")

    product = get_object_or_404(Product, id=product_id)
    product_name = product.name
    product.delete()
    messages.success(request, f"Produto '{product_name}' excluído com sucesso.")
    return redirect("landing:backoffice_dashboard")


@login_required
def backoffice_logout(request):
    logout(request)
    return redirect("landing:backoffice_login")
