from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = "inventory"
urlpatterns = [
    path("", views.IndexView, name="index"),
    path("all/", views.AllItemIndexView, name="all_items"),

    path("rooms/", views.RoomIndexView, name="room_index"),
    path("rooms/<int:pk>/", views.RoomDetailView, name="room_detail"),
    path("rooms/<int:room_pk>/newStorage/", views.NewStorageView, name="new_storage_from_room"),

    path("items/<int:pk>/", views.ItemDetailView, name="item_detail"),
    path("items/<int:pk>/edit/", views.ItemEditView, name="item_edit"),
    path("items/confirm_location/", views.confirm_item_location, name="confirm_item_location"),
    path("items/report_missing/", views.report_item_missing, name="report_item_missing"),
    path("items/update_location/", views.update_item_location, name="update_item_location"),
    path("items/update_qty/", views.update_item_quantity, name="update_item_quantity"),
    path("items/", views.ItemIndexView, name="item_index"),
    path("items/newItem/", views.NewItemView, name="new_item"),

    path("storage/", views.StorageIndexView, name="storage_index"),
    path("storage/<int:pk>/", views.StorageDetailView, name="storage_detail"),
    path("storage/<int:storage_pk>/newItem/", views.NewItemView, name="new_item_from_storage"),
    path("storage/<int:storage_pk>/edit/", views.EditStorage, name="edit_storage"),
    path("storage/newStorage/", views.NewStorageView, name="new_storage"),

    path("search/", login_required(views.SearchResultsView.as_view()), name="search_results"),

    path("reorderList/", views.ReorderView, name="reorder_list"),
    path("missingItems/", views.MissingItemIndexView, name="missing_list"),

]
