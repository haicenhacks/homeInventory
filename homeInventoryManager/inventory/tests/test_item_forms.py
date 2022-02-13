from django.test import TestCase

from inventory.forms import ItemForm
from inventory.models import Room, Storage, Item
# from django.http import HttpRequest
# from django_webtest import WebTest
# from mixer.backend.django import mixer
import datetime

import pytest


@pytest.mark.django_db
class test_ItemForm(TestCase):
    def setUp(self):
        """Set up base objects."""
        test_room = Room.objects.create(name="test room1")
        self.test_storage = Storage.objects.create(name="test containerITEM", room=test_room)

    def test_name_too_short(self):
        """Test name shorter than 3 characters."""
        form = ItemForm(data={"name": "a", "location": self.test_storage.pk, "quantity": 1, "par_value": 1, "condition": "Good", "missing": False})
        self.assertEqual(form.errors["name"], ["Item name should be at least 3 characters"])
        self.assertFalse(form.is_valid())

    def test_name_valid_length(self):
        """Test name is more than 3 characters."""
        form = ItemForm(data={"name": "test_name_valid_length", "location": self.test_storage.pk, "quantity": 1, "par_value": 1, "condition": "Good", "missing": False})
        self.assertTrue(form.is_valid())

    def test_condition_invalid(self):
        """Test condition not in dropdown."""
        data = {"name": "abcde",
                "location": self.test_storage.pk,
                "quantity": 1,
                "par_value": 1,
                "condition": "test",
                "missing": False}
        form = ItemForm(data)
        self.assertIn("Select a valid choice. test is not one of the available choices.", form.errors["condition"], )
        self.assertFalse(form.is_valid())

    def test_invalid_location(self):
        """Test location that does not exist."""
        data = {"name": "abcde",
                "location": 15,
                "quantity": 1,
                "par_value": 1,
                "condition": "Good",
                "missing": False}
        form = ItemForm(data)
        self.assertFalse(form.is_valid())

    def test_valid_location(self):
        """Test location that does exist."""
        data = {"name": "abcde",
                "location": self.test_storage,
                "quantity": 1,
                "par_value": 1,
                "condition": "Good",
                "missing": False}
        form = ItemForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_quantity(self):
        """Test negative quantity."""
        data = {"name": "abcde",
                "location": self.test_storage,
                "quantity": -1,
                "par_value": 1,
                "condition": "Good",
                "missing": False}
        form = ItemForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("Quantity cannot be negative", form.errors["quantity"])

    def test_invalid_par_value(self):
        """Test negative par value."""
        data = {"name": "abcde",
                "location": self.test_storage,
                "quantity": 1,
                "par_value": -1,
                "condition": "Good",
                "missing": False}
        form = ItemForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("Par value cannot be negative", form.errors["par_value"])

    def test_all_fields_valid(self):
        """Test that all fields are valid."""
        data = {"name": "all_fields_valid",
                "location": self.test_storage,
                "quantity": 1,
                "par_value": 1,
                "purchase_date": "2021-06-01",
                "asset_tag": "X000101",
                "notes": "test notes",
                "condition": "Good",
                "missing": False,
                }
        form = ItemForm(data)
        self.assertTrue(form.is_valid())
        form.save()
        this_item = Item.objects.get(name="all_fields_valid")
        self.assertEqual(this_item.name, data["name"])
        self.assertEqual(this_item.location, data["location"])
        self.assertEqual(this_item.quantity, data["par_value"])
        self.assertEqual(this_item.par_value, data["par_value"])
        self.assertEqual(this_item.purchase_date, datetime.date(2021, 6, 1))
        self.assertEqual(this_item.asset_tag, data["asset_tag"])
        self.assertEqual(this_item.notes, data["notes"])
        self.assertEqual(this_item.condition, data["condition"])
        self.assertEqual(this_item.missing, False)
