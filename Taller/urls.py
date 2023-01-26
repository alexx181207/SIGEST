from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from . import views, list_views, ajax_views

urlpatterns = [
    # post views
    
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
        r"^buscar/servicio/ajax/$", ajax_views.list_json, name="servicio_encontrar"
    ),
    
    re_path(
        r"^buscar/servicio/ajax/(?P<prefijo>\w+)/(?P<servicio>\w+)/(?P<fechainicio>\d{2}/\d{2}/\d{4})-(?P<fechafin>\d{2}/\d{2}/\d{4})/",
        ajax_views.list_json,
        name="servicio_encontrar",
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
]
