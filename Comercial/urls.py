from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("create/", views.CrearOrden.as_view(), name="orden_create"),
    path(
        "create/pdf_orden/",
        views.PdfView.as_view(),
        {"plantilla": "Comercial/pdf_orden.html"},
        name="pdf_orden",
    ),
    path(
        "create/pdf_garantía/",
        views.PdfView.as_view(),
        {"plantilla": "Comercial/pdf_garantia.html"},
        name="pdf_garantia",
    ),
    path(
        "create/imp_orden/",
        views.PDFOrden.as_view(),
        {"plantilla": "orden/orden_nueva.html"},
        name="imp_orden",
    ),
    path(
        "create/imp_garantia/",
        views.PDFOrden.as_view(),
        {"plantilla": "orden/carta.html"},
        name="imp_garantia",
    ),
    path("create/gestion_orden/", views.PDFGestion.as_view(), name="gestion_orden"),
  
    re_path(
        r"^ordenprimaria/(?P<pk>[0-9]+)/$",
        views.UpdateOrder.as_view(),
        name="update_order",
    ),
    re_path(
        r"^ordenprimaria/(?P<pk>[0-9]+)/delete/$",
        views.DeleteOrder.as_view(),
        name="delete_order",
    ),
   
    re_path(
        r"^index/gestion_telefono/(?P<pk>\d+)/$",
        views.OrdenLlamada.as_view(),
        name="gestion_telefono_llamar",
    ),
    re_path(
        r"^create/pdf_orden/(?P<ordenprimaria_id>\d+)/$",
        views.reimprimir_orden,
        {"plantilla": "Comercial/pdf_orden.html"},
        name="reimprimir_orden",
    ),
    re_path(r"^cerrar/(?P<pk>\d+)/$", views.CerrarOrden.as_view(), name="orden_close"),
]
