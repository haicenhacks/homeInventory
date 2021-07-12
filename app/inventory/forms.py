from django.forms import ModelForm
# from django.forms import inlineformset_factory
from django import forms
from .models import Item, Storage, CustomUser
# from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from django.shortcuts import get_object_or_404
import datetime


class DateInput(forms.DateInput):
    input_type = "date"


class ItemForm(ModelForm):
    def __init__(self, *args, **kwargs):
        """Initialize form."""
        super(ItemForm, self).__init__(*args, **kwargs)
        instance = getattr(self, "instance", None)

        if instance and instance.pk:
            self.fields["asset_tag"].disabled = True
            self.is_instance = True

        else:
            self.is_instance = False

    error_css_class = "error"
    required_css_class = "required"

    class Meta:
        """Meta class to handle form fields and widgets."""

        model = Item
        fields = ["name", "location", "quantity", "par_value",
                  "notes", "image", "condition", "asset_tag", "purchase_date", "model_number", "serial_number"]
        widgets = {"purchase_date": DateInput()}

    def validate_purchase_date(self, purchase_date=None):
        """Validate purchase date."""
        if purchase_date:
            if not isinstance(purchase_date, datetime.date):
                # user should not see this error if the datepicker widget is used
                self.add_error("purchase_date", "Invalid date format")
            else:
                return purchase_date

    def validate_asset_tag(self, asset_tag):
        """Validate asset tag."""
        if asset_tag and not self.is_instance:
            item_qs = Item.objects.filter(asset_tag__exact=asset_tag)
            if len(item_qs) > 0:
                self.add_error("asset_tag", "This asset tag already exists in database")
            return asset_tag

    def validate_name(self, name):
        """Validate item name."""
        if len(name) < 3:
            self.add_error("name", "Item name should be at least 3 characters")
        else:
            return name

    def validate_quantity(self, quantity):
        """Validate quantity is not negative or zero."""
        if quantity < 0:
            self.add_error("quantity", "Quantity cannot be negative")
        else:
            return quantity

    def validate_par_value(self, par_value):
        """Validate that par_value is not negative."""
        if par_value < 0:
            self.add_error("par_value", "Par value cannot be negative")
        else:
            return par_value

    def validate_condition(self, condition):
        """Validate condition."""
        if not condition:
            self.add_error("condition", "Condition is required")
        else:
            return condition

    def validate_location(self, location):
        """Validate that location exists."""
        if not location:
            self.add_error("location", "This location is invalid")
            return None
        else:
            return location

    def clean(self):
        """Clean the submitted form data."""
        super(ItemForm, self).clean()

        name = self.cleaned_data.get("name")
        location = self.cleaned_data.get("location")
        quantity = self.cleaned_data.get("quantity")
        par_value = self.cleaned_data.get("par_value")
        purchase_date = self.cleaned_data.get("purchase_date")
        # serial_number = self.cleaned_data.get("serial_number")
        # notes = self.cleaned_data.get("notes")
        # image = self.cleaned_data.get("image")
        condition = self.cleaned_data.get("condition")
        asset_tag = self.cleaned_data.get("asset_tag")

        self.cleaned_data["name"] = self.validate_name(name)
        self.cleaned_data["location"] = self.validate_location(location)
        self.cleaned_data["quantity"] = self.validate_quantity(quantity)
        self.cleaned_data["par_value"] = self.validate_par_value(par_value)
        self.cleaned_data["condition"] = self.validate_condition(condition)
        self.cleaned_data["purchase_date"] = self.validate_purchase_date(purchase_date)
        self.cleaned_data["asset_tag"] = self.validate_asset_tag(asset_tag)

        return self.cleaned_data


class StorageForm(ModelForm):
    class Meta:
        """Meta class to handle form fields and widgets."""

        model = Storage
        fields = ["name", "type", "description", "room", ]


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        """Meta class to handle form fields and widgets."""

        model = CustomUser
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        """Meta class to handle form fields and widgets."""

        model = CustomUser
        fields = ("username", "email")
