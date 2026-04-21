from django.urls import path

from .views import (
    BackofficeLoginView,
    backoffice_dashboard,
    backoffice_logout,
    backoffice_product_create,
    backoffice_product_delete,
    backoffice_product_edit,
    backoffice_product_toggle_featured,
    healthz,
    home,
    privacy_policy,
    terms_conditions,
)

app_name = "landing"

urlpatterns = [
    path("", home, name="home"),
    path("healthz/", healthz, name="healthz"),
    path("politica-de-privacidade/", privacy_policy, name="privacy_policy"),
    path("termos-e-condicoes/", terms_conditions, name="terms_conditions"),
    path("adm/login/", BackofficeLoginView.as_view(), name="backoffice_login"),
    path("adm/logout/", backoffice_logout, name="backoffice_logout"),
    path("adm/", backoffice_dashboard, name="backoffice_dashboard"),
    path("adm/produtos/novo/", backoffice_product_create, name="backoffice_product_create"),
    path("adm/produtos/<int:product_id>/editar/", backoffice_product_edit, name="backoffice_product_edit"),
    path("adm/produtos/<int:product_id>/toggle-destaque/", backoffice_product_toggle_featured, name="backoffice_product_toggle_featured"),
    path("adm/produtos/<int:product_id>/excluir/", backoffice_product_delete, name="backoffice_product_delete"),
]
