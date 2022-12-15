from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from . import (
    views,
    list_views,
    ajax_views,
)

urlpatterns = [
    # post views
    path("", views.loggin, name="loggin"),
    path("index/", views.Index.as_view(), name="index"),
    path(
        "index/gestion_telefono/",
        list_views.GestionTelefono.as_view(),
        name="gestion_telefono",
    ),
    path(
        "password/change/form/", views.ChangePassword.as_view(), name="change_password"
    ),
    path(
        "index/list/reparadas/",
        list_views.ListadoReparadas.as_view(),
        name="ordenes_reparadas",
    ),
    path(
        "index/list/update/",
        list_views.ListUpdates.as_view(),
        name="list_updates",
    ),
    path("index/list/", list_views.ListadoOrdenesMixin.as_view(), name="ordenes_lista"),
    path(
        "index/list/dia/", list_views.TrabajosDiarios.as_view(), name="trabajos_diarios"
    ),
    path(
        "index/list/defectar/fuera/termino",
        list_views.ListSinDefectar.as_view(),
        name="defectar_fuera_termino",
    ),
    path(
        "index/list/reparar/fuera/termino",
        list_views.ListSinReparar.as_view(),
        name="reparar_fuera_termino",
    ),
    path(
        "index/list/entregar/",
        list_views.EntregarOrdenesTaller.as_view(),
        name="ordenes_entregar",
    ),
    path(
        "index/list/confirmar/",
        list_views.ConfirmarOrdenesTaller.as_view(),
        name="ordenes_confirmar",
    ),
    path(
        "index/list/pendientes/",
        list_views.ListadoPendientes.as_view(),
        name="ordenes_pendientes",
    ),
    path(
        "index/list/warranty/", list_views.WarrantyList.as_view(), name="warranty_list"
    ),
    path(
        "index/list/pendientes/edades",
        list_views.ordenesEdades,
        name="ordenes_pendientes_edades",
    ),
    path("index/list/reg_tfa/", list_views.RegistroTFA.as_view(), name="registro_tfa"),
    path("index/list/reg_tb/", list_views.RegistroTB.as_view(), name="registro_tb"),
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
    path("pentregar/", ajax_views.entregar_taller, name="orden_entregar_taller"),
    path("pconfirmar/", ajax_views.confirmar_taller, name="orden_confirmar_taller"),
    path(
        "buscar/servicio/", ajax_views.BuscarServicios.as_view(), name="servicio_form"
    ),
    path(
        "consumir/recurso/",
        ajax_views.consumir_recursos,
        name="agregar_consumo_recurso",
    ),
    path(
        "recursos/consumidos/",
        ajax_views.recursos_consumidos,
        name="recursos_consumidos",
    ),
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
        r"^buscar/servicio/ajax/$", ajax_views.list_json, name="servicio_encontrar"
    ),
    re_path(
        r"^index/gestion_telefono/(?P<pk>\d+)/$",
        views.OrdenLlamada.as_view(),
        name="gestion_telefono_llamar",
    ),
    re_path(
        r"^buscar/servicio/ajax/(?P<prefijo>\w+)/(?P<servicio>\w+)/(?P<fechainicio>\d{2}/\d{2}/\d{4})-(?P<fechafin>\d{2}/\d{2}/\d{4})/",
        ajax_views.list_json,
        name="servicio_encontrar",
    ),
    path("logout/", views.loggedout, name="logout"),
    re_path(r"^accounts/login/$", views.user_login, name="login"),
    re_path(
        r"^create/pdf_orden/(?P<ordenprimaria_id>\d+)/$",
        views.reimprimir_orden,
        {"plantilla": "Comercial/pdf_orden.html"},
        name="reimprimir_orden",
    ),
    re_path(
        r"^index/list/entregar/(?P<ordenprimaria_id>\d+)/$",
        list_views.EntregaOrdenTaller,
        name="orden_entrega",
    ),
    re_path(
        r"^index/list/confirmar/(?P<ordenprimaria_id>\d+)/$",
        list_views.ConfirmaOrdenTaller,
        name="orden_confirma",
    ),
    re_path(
        r"^defectar/(?P<pk>\d+)/$",
        views.RepararOrden.as_view(),
        name="orden_lista_defectadas",
    ),
    re_path(
        r"^date/close/(?P<pk>\d+)/$",
        views.OrderwarrantyView.as_view(),
        name="orden_close_date",
    ),
    re_path(r"^cerrar/(?P<pk>\d+)/$", views.CerrarOrden.as_view(), name="orden_close"),
    # url(r'^buscar/orden/$', views.buscarorden, name='orden_form'),
    # url(r'^buscar/servicio/ajax/$', ajax_views.buscarservicio, name='servicio_encontrar'),
    # url(r'^buscar/orden/(?P<orden>\d+)/(?P<estado>\d+)/(?P<fechainicio>\d+)/(?P<fechafin>\d+)$', views.buscarorden, name='orden_buscar'),
    # url(r'^buscar/servicio/(?P<servicio>\d+)/(?P<estado>\d+)/(?P<fechainicio>\d+)/(?P<fechafin>\d+)/$', views.buscarservicio, name='servicio_buscar'),
    # url(r'^pentregar/detail/(?P<pk>\d+)/$', views.EntregarTaller.as_view(), name='orden_entregar_taller'),
    # url(r'^reparar/$', views.RepararOrden.as_view(), name='orden_lista_reparadas'),
    # url(r'^index/list/defectacion/$', views.listadoOrdenesSinDefectar, name='ordenes_defec'),
    # url(r'^pdf/(?P<ordenprimaria_id>\d+)/$', files_views.gen_pdf, name='pdf_files'),
]
