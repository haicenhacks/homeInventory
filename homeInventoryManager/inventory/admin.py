from django.contrib import admin

# Register your models here.
from .models import Room, Storage, Item, Document, CustomUser

class DocumentInlineAdmin(admin.StackedInline):
    model = Document
    extra = 1


class ItemAdmin(admin.ModelAdmin):
    model = Item
    list_display = ("name", "location", "quantity", "asset_tag")
    list_filter = ["location__room", "location__name", "missing", "purchase_date", ('image', admin.EmptyFieldListFilter)]
    search_fields = ["name", "asset_tag", "id"]
    inlines = [DocumentInlineAdmin]


class DocumentAdmin(admin.ModelAdmin):
    model = Document
    list_display = ("item", "type", "displayName", "file")


class StorageAdmin(admin.ModelAdmin):
    model = Storage
    list_display = ["room", "name", "type", "description"]
    list_filter = ["room", "type"]


admin.site.register(Room)
admin.site.register(Storage, StorageAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(CustomUser)
admin.site.site_title = "Home Inventory Admin"
admin.site.site_header = "Home Inventory"
admin.site.index_title = "Site Settings"
