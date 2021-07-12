# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
# from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.db.models import F, Q
from django.forms import inlineformset_factory
from django.forms.utils import ErrorList
from django.contrib.auth.decorators import login_required
# from django.utils import timezone
# from .forms import UploadFileForm
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect
# from itertools import chain
# import datetime

from .models import Item, CustomUser, Room, Storage, Document
from .forms import ItemForm, StorageForm


class DivErrorList(ErrorList):
    def __str__(self):
        """Return string representation."""
        return self.as_divs()

    def as_divs(self):
        """Return errors as pre-formatted divs."""
        if not self:
            return ""
        return '<div class="errorlist">%s</div>' % "".join(['<div class="alert alert-danger error">%s</div>' % e for e in self])


@login_required
def IndexView(request):
    """Index view."""
    template_name = "inventory/index.html"
    queryset = Room.objects.order_by("name")
    context = {"rooms": queryset}

    return render(request, template_name, context)


@login_required
def AllItemIndexView(request):
    item_qs = Item.objects.all()
    template_name = "inventory/item_list.html"

    return render(request, template_name, {"item_qs": item_qs})


@login_required
def RoomIndexView(request):
    rooms = Room.objects.all()
    return render(request, "inventory/room_index.html", {"rooms": rooms})


@login_required
def RoomDetailView(request, pk):
    room = get_object_or_404(Room, pk=pk)
    queryset = Storage.objects.filter(room=pk)
    items = [x.item_set.all().order_by("quantity")[:5] for x in queryset]
    context = {"storage_items": zip(queryset, items), "room": room}
    template_name = "inventory/room_detail.html"

    return render(request, template_name, context)


@login_required
def ItemDetailView(request, pk):
    item = get_object_or_404(Item, pk=pk)
    template_name = "inventory/item_detail.html"
    all_storage_locs = Storage.objects.all()
    docs = Document.objects.filter(item=pk)
    docs.group_by = ["type"]

    doctypes = set([x.type for x in docs])
    all_users = CustomUser.objects.all()
    context = {"item": item,
               "all_storage_locs": all_storage_locs,
               "docs": docs,
               "doctypes": doctypes,
               "all_users": all_users}

    return render(request, template_name, context)


@login_required
def ItemEditView(request, pk):
    this_item = Item.objects.get(pk=pk)
    DocumentFormSet = inlineformset_factory(Item, Document, fields=["file", "displayName", "type"], extra=1)
    formset = DocumentFormSet(instance=this_item)
    # for d in formset:
    # print(d["file"].value())
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=this_item)
        docforms = DocumentFormSet(request.POST, request.FILES, instance=this_item)
        print(len(docforms))
        print(form.is_valid(), docforms.is_valid())
        if form.is_valid() and docforms.is_valid():

            form.save()
            docs = docforms.save(commit=False)
            for doc in docs:
                doc.save()

            messages.add_message(request, messages.SUCCESS, "Item updated")
            return HttpResponseRedirect(reverse("inventory:item_detail", kwargs={"pk": this_item.pk}))
        else:
            context = {"form": form}
    else:

        form = ItemForm(instance=this_item)
        context = {"form": form,
                   "docform": formset
                   }
    return render(request, "inventory/edit_item_form.html", context)


@login_required
def confirm_item_location(request):
    """Ajax view for confirming item is in correct location."""
    if request.method == "POST":
        pk = request.POST["pk"]
        this_item = get_object_or_404(Item, pk=pk)
        this_item.confirm_location()
        return HttpResponse("success")
    else:
        return HttpResponse(status=405)


@login_required
@csrf_protect
def report_item_missing(request):
    """Ajax view for reporting item is missing."""
    if request.method == "POST":
        pk = request.POST["pk"]
        this_item = get_object_or_404(Item, pk=pk)
        this_item.report_missing()
        return HttpResponse("success")
    else:
        return HttpResponse(status=405)


@login_required
@csrf_protect
def update_item_location(request):
    """View for updating item location."""
    if request.method == "POST":
        item_pk = request.POST["item_id"]
        if item_pk:
            this_item = get_object_or_404(Item, pk=item_pk)
            new_loc_pk = request.POST["new_loc_id"]
            this_item.update_location(new_loc_pk=new_loc_pk)
            messages.add_message(request, messages.SUCCESS, "location updated")
        else:
            return HttpResponse(status=404)
        return HttpResponse("success")
    elif request.method == "POST":
        return HttpResponse(status=405)
    else:
        return HttpResponse(status=405)


@login_required
@csrf_protect
def update_item_quantity(request):
    """Ajax view for updating item quantity."""
    if request.method == "POST":
        item_pk = request.POST["item_id"]
        this_item = get_object_or_404(Item, pk=item_pk)
        new_qty = request.POST["new_qty"]
        this_item.update_quantity(new_qty=new_qty)
        messages.add_message(request, messages.SUCCESS, "quantity updated")

        return HttpResponse("success")
    else:
        return HttpResponse(status=405)


@login_required
def ItemIndexView(request):
    item_qs = Item.objects.all()
    template_name = "inventory/item_list.html"

    return render(request, template_name, {"item_qs": item_qs})


@login_required
def NewItemView(request, storage_pk=None):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, error_class=DivErrorList)
        if form.is_valid():
            new_item = form.save()
            if storage_pk:
                return HttpResponseRedirect(reverse("inventory:storage_detail", kwargs={"pk": storage_pk}))
            return HttpResponseRedirect(reverse("inventory:item_detail", kwargs={"pk": new_item.pk}))
        else:

            context = {"form": form}
            return render(request, "inventory/edit_item_form.html", context)

    else:
        form = ItemForm()
        if storage_pk:
            form = ItemForm(initial={"location": storage_pk})
        context = {"form": form}

        return render(request, "inventory/edit_item_form.html", context)


@login_required
def StorageIndexView(request):
    queryset = Storage.objects.all()
    items = [x.item_set.all().order_by("quantity")[:5] for x in queryset]
    print("qs: ", queryset)
    print("it: ", items)
    template_name = "inventory/storage_index.html"

    return render(request, template_name, {"context": zip(queryset, items)})


@login_required
def StorageDetailView(request, pk):
    storage = get_object_or_404(Storage, pk=pk)
    template_name = "inventory/storage_detail.html"

    return render(request, template_name, {"storage": storage})


@login_required
def EditStorage(request, storage_pk):
    this_storage = Storage.objects.get(pk=storage_pk)

    if request.method == "POST":
        form = StorageForm(request.POST, instance=this_storage)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Storage updated')
            return HttpResponseRedirect(reverse("inventory:storage_detail", kwargs={"pk": storage_pk}))
        else:
            context = {"form": form}
            return render(request, "inventory/edit_storage_form.html", context)

    else:
        form = StorageForm(instance=this_storage)
        context = {"form": form}
        return render(request, "inventory/edit_storage_form.html", context)


@login_required
def NewStorageView(request, room_pk=None):
    if request.method == "POST":
        form = StorageForm(request.POST)
        if form.is_valid():
            form.save()
            if room_pk:
                return HttpResponseRedirect(reverse("inventory:room_detail", kwargs={"pk": room_pk}))
            return HttpResponseRedirect(reverse("inventory:index"))
        else:
            context = {"form": form, "new_storage": True}
            return render(request, "inventory/edit_storage_form.html", context)

    else:
        form = StorageForm()
        if room_pk:
            form = StorageForm(initial={"room": room_pk})
        context = {"form": form, "new_storage": True}
        return render(request, "inventory/edit_storage_form.html", context)


class SearchResultsView(generic.ListView):
    model = Item
    template_name = "inventory/search_results.html"

    def get_1context_data(self, *args, **kwargs):
        """Return location, rooms, and object list to search result view."""
        context = super(generic.ListView, self).get_context_data(*args, **kwargs)

        locations = []
        locs = [x.location for x in self.get_queryset()]
        rooms = []
        for loc in locs:
            if loc not in locations:

                locations.append(loc)

            if loc.room not in rooms:
                rooms.append(loc.room)

        context = {"storage_list": locations, "object_list": self.get_queryset(), "rooms": rooms, "room_row_span": len(locations)}

        return context

    def get_queryset(self):
        """Return sorted queryset of items matching search criteria."""
        query = self.request.GET.get("q")
        item_list = Item.objects.filter(name__icontains=query)
        item_list.group_by = ["location", "location.room"]
        qs = sorted(item_list,
                    key=lambda instance: instance.location.name,
                    reverse=True)

        return qs


@login_required
def ReorderView(request):
    item_qs = Item.objects.filter(Q(quantity__lt=F("par_value")) | Q(quantity=0))
    context = {"item_qs": item_qs}

    return render(request, "inventory/reorder_list.html", context)


@login_required
def MissingItemIndexView(request):
    item_qs = Item.objects.filter(missing=True)
    all_storage_locs = Storage.objects.all()
    context = {"item_qs": item_qs, "all_storage_locs": all_storage_locs}

    return render(request, "inventory/missing_item_list.html", context)
