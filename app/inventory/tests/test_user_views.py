# import datetime

from django.test import TestCase, Client
# from django.utils import timezone
from django.urls import reverse
# from django.contrib.auth.models import User
from inventory.models import Room, Storage, Item, CustomUser
# import json
# from django.contrib.auth import get_user_model


class TestUserViews(TestCase):
    def setUp(self):
        """Test setup."""
        self.login()
        self.client = Client()
        self.credentials = {'username': "testuser", 'password': 'foo'}

        self.user = CustomUser.objects.create_user(email='normal@user.com', username=self.credentials['username'])
        self.user.set_password(self.credentials['password'])
        self.user.save()

        self.staff_user = CustomUser.objects.create_user(email='staff@user.com', username="staffuser", password='foo', is_staff=True)
        self.test_room = Room.objects.create(name="test room")
        self.test_storage1 = Storage.objects.create(name="test container1", room=self.test_room)
        self.test_storage2 = Storage.objects.create(name="test container2", room=self.test_room)
        self.test_storage3 = Storage.objects.create(name="test container3", room=self.test_room)
        # print(self.test_storage1.pk)
        self.item1 = Item(name="Test Item #1", location=self.test_storage1, quantity=1,
                          par_value=1, purchase_date="2021-06-01",
                          asset_tag="001", notes="some notes about item 1",
                          image=None, condition="Good",
                          model_number="A427", serial_number="551", warranty_expire_date=None,
                          pk=1
                          )
        self.item1.save()
        # print(self.item1)

        self.index_url = reverse("inventory:index")
        self.all_items_url = reverse("inventory:all_items")
        self.room_detail_url = reverse("inventory:room_detail", kwargs={'pk': self.test_room.pk})
        self.new_storage_from_room_url = reverse("inventory:new_storage_from_room", kwargs={'room_pk': self.test_room.pk})
        self.item_detail_url = reverse("inventory:item_detail", kwargs={'pk': self.item1.pk})
        self.item_edit_url = reverse("inventory:item_edit", kwargs={'pk': self.item1.pk})
        self.confirm_item_location_url = reverse("inventory:confirm_item_location")
        self.report_item_missing_url = reverse("inventory:report_item_missing")
        self.update_item_location_url = reverse("inventory:update_item_location")
        self.update_item_quantity_url = reverse("inventory:update_item_quantity")
        self.item_index_url = reverse("inventory:item_index")
        self.new_item_url = reverse("inventory:new_item")
        self.storage_index_url = reverse("inventory:storage_index")
        self.storage_detail_url = reverse("inventory:storage_detail", kwargs={'pk': self.test_storage1.pk})
        self.new_item_from_storage_url = reverse("inventory:new_item_from_storage", kwargs={'storage_pk': self.test_storage1.pk})
        self.edit_storage_url = reverse("inventory:edit_storage", kwargs={'storage_pk': self.test_storage1.pk})
        self.new_storage_url = reverse("inventory:new_storage")
        self.search_results_url = reverse("inventory:search_results")
        self.reorder_url = reverse("inventory:reorder_list")
        self.missing_items_url = reverse("inventory:missing_list")

    def login(self):
        """Log user in for tests that require it."""
        credentials = {'username': "testuser", 'password': 'foo'}

        self.logged_in = self.client.login(username=credentials['username'], password=credentials['password'])

    def test_login(self):
        """Test log in."""
        self.login()
        logged_in = self.client.login(username=self.credentials['username'], password=self.credentials['password'])
        self.assertTrue(logged_in)

    def test_logout(self):
        """Test log out function."""
        self.login()
        logged_in = self.client.login(username=self.credentials['username'], password=self.credentials['password'])
        self.assertTrue(logged_in)
        logged_in = self.client.logout()
        self.assertFalse(logged_in)

    def test_empty_GET(self):
        """Test empty url resolves."""
        self.login()
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/index.html')

    def test_all_item_url(self):
        """Test all/ resolves."""
        self.login()
        response = self.client.get(self.all_items_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/item_list.html')

    def test_room_detail(self):
        """Test room detail resolves."""
        self.login()
        response = self.client.get(self.room_detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/room_detail.html')

    def test_item_detail(self):
        """Test item detail resolves."""
        self.login()
        response = self.client.get(self.item_detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/item_detail.html')

    def test_item_edit(self):
        """Test item edit resolves."""
        self.login()
        response = self.client.get(self.item_edit_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/edit_item_form.html')

    def test_confirm_item_location_POST(self):
        """Test confirm item location resolves."""
        self.login()
        response = self.client.post(self.confirm_item_location_url, {'pk': self.item1.pk})
        self.assertEquals(response.status_code, 200)

    def test_confirm_item_location_GET(self):
        """Test confirm item location resolves."""
        self.login()
        response = self.client.get(self.confirm_item_location_url, {'pk': self.item1.pk})
        self.assertEquals(response.status_code, 405)

    def test_report_item_missing_GET(self):
        """Test report item missing resolves."""
        self.login()
        response = self.client.get(self.report_item_missing_url, {'pk': self.item1.pk})
        self.assertEquals(response.status_code, 405)

    def test_report_item_missing_POST(self):
        """Test report item missing resolves."""
        self.login()
        response = self.client.post(self.report_item_missing_url, {'pk': self.item1.pk})
        self.assertEquals(response.status_code, 200)

    def test_update_item_location_POST(self):
        """Test update item location resolves."""
        self.login()
        self.assertEquals(self.item1.location.pk, self.test_storage1.pk)
        response = self.client.post(self.update_item_location_url, {"item_id": self.item1.pk, "new_loc_id": self.test_storage2.pk})
        item1 = Item.objects.get(pk=self.item1.pk)
        self.assertEquals(item1.location.pk, self.test_storage2.pk)

        self.assertEquals(response.status_code, 200)

    def test_update_item_location_GET(self):
        """Test update item location resolves."""
        self.login()
        self.assertEquals(self.item1.location.pk, self.test_storage1.pk)
        response = self.client.get(self.update_item_location_url, {"item_id": self.item1.pk, "new_loc_id": self.test_storage2.pk})
        item1 = Item.objects.get(pk=self.item1.pk)
        self.assertNotEqual(item1.location.pk, self.test_storage2.pk)
        self.assertEqual(item1.location.pk, self.test_storage1.pk)
        self.assertEqual(response.status_code, 405)

    def test_update_item_quantity_POST(self):
        """Test update item quantity resolves."""
        self.login()
        self.assertEqual(self.item1.quantity, 1)
        response = self.client.post(self.update_item_quantity_url, {"item_id": self.item1.pk, "new_qty": 5})
        self.assertEquals(response.status_code, 200)
        item1 = Item.objects.get(pk=self.item1.pk)
        self.assertEqual(item1.quantity, 5)

    def test_update_item_quantity_GET(self):
        """Test update item quantity resolves."""
        self.login()
        self.assertEqual(self.item1.quantity, 1)
        response = self.client.get(self.update_item_quantity_url, {"item_id": self.item1.pk, "new_qty": 5})
        self.assertEquals(response.status_code, 405)
        item1 = Item.objects.get(pk=self.item1.pk)
        self.assertEqual(item1.quantity, 1)

    def test_item_index(self):
        """Test item_index resolves."""
        self.login()
        response = self.client.get(self.item_index_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/item_list.html')

    def test_storage_detail(self):
        """Test storage_detail resolves."""
        self.login()
        response = self.client.get(self.storage_detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/storage_detail.html')

    def test_storage_index(self):
        """Test storage_index resolves."""
        self.login()
        response = self.client.get(self.storage_index_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/storage_index.html')

    def test_new_item(self):
        """Test new_item resolves."""
        self.login()
        response = self.client.get(self.new_item_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/edit_item_form.html')

    def test_new_item_from_storage(self):
        """Test new_item_from_storage resolves."""
        self.login()
        response = self.client.get(self.new_item_from_storage_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/edit_item_form.html')

    def test_new_storage(self):
        """Test new_storage resolves."""
        self.login()
        response = self.client.get(self.new_storage_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/edit_storage_form.html')

    def test_new_storage_from_room(self):
        """Test new_storage_from_room resolves."""
        self.login()
        response = self.client.get(self.new_storage_from_room_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/edit_storage_form.html')

    def test_search(self):
        """Test search resolves."""
        self.login()
        response = self.client.get(self.search_results_url, {'q': "Test Item"})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/search_results.html')

    def test_reorder_list(self):
        """Test reorder_list resolves."""
        self.login()
        response = self.client.get(self.reorder_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/reorder_list.html')

    def test_missing_items(self):
        """Test missing_items resolves."""
        self.login()
        response = self.client.get(self.missing_items_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/missing_item_list.html')

    # begin no-login
    def test_empty_GET_no_login(self):
        """Test empty url returns 302 without login."""
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 302)

    def test_all_item_url_no_login(self):
        """Test all/ returns 302 without login."""
        response = self.client.get(self.all_items_url)
        self.assertEquals(response.status_code, 302)

    def test_room_detail_no_login(self):
        """Test room list returns 302 without login."""
        response = self.client.get(self.room_detail_url)
        self.assertEquals(response.status_code, 302)

    def test_item_detail_no_login(self):
        """Test item detail returns 302 without login."""
        response = self.client.get(self.item_detail_url)
        self.assertEquals(response.status_code, 302)

    def test_item_edit_no_login(self):
        """Test item edit returns 302 without login."""
        response = self.client.get(self.item_edit_url)
        self.assertEquals(response.status_code, 302)

    def test_confirm_item_location_POST_no_login(self):
        """Test confirm item location returns 302 without login."""
        response = self.client.post(self.confirm_item_location_url, {'pk': self.item1.pk})
        self.assertEquals(response.status_code, 302)

    def test_confirm_item_location_GET_no_login(self):
        """Test confirm item location returns 302 without login."""
        response = self.client.get(self.confirm_item_location_url, {'pk': self.item1.pk})
        self.assertEquals(response.status_code, 302)

    def test_report_item_missing_GET_no_login(self):
        """Test report item missing returns 302 without login."""
        response = self.client.get(self.report_item_missing_url, {'pk': self.item1.pk})
        self.assertEquals(response.status_code, 302)

    def test_report_item_missing_POST_no_login(self):
        """Test report item missing returns 302 without login."""
        response = self.client.post(self.report_item_missing_url, {'pk': self.item1.pk})
        self.assertEquals(response.status_code, 302)

    def test_update_item_location_POST_no_login(self):
        """Test update item location returns 302 without login."""
        self.assertEquals(self.item1.location.pk, self.test_storage1.pk)
        response = self.client.post(self.update_item_location_url, {"item_id": self.item1.pk, "new_loc_id": self.test_storage2.pk})
        item1 = Item.objects.get(pk=self.item1.pk)
        self.assertEquals(item1.location.pk, self.test_storage1.pk)

        self.assertEquals(response.status_code, 302)

    def test_update_item_location_GET_no_login(self):
        """Test update item location returns 302 without login."""
        self.assertEquals(self.item1.location.pk, self.test_storage1.pk)
        response = self.client.get(self.update_item_location_url, {"item_id": self.item1.pk, "new_loc_id": self.test_storage2.pk})
        self.assertEqual(response.status_code, 302)

    def test_update_item_location_GET_no_login_verify_no_changes(self):
        """Test update item location does not make changes with an unauthenticated get."""
        self.assertEquals(self.item1.location.pk, self.test_storage1.pk)
        response = self.client.get(self.update_item_location_url, {"item_id": self.item1.pk, "new_loc_id": self.test_storage2.pk})
        self.assertEquals(response.status_code, 302)
        item1 = Item.objects.get(pk=self.item1.pk)
        self.assertEqual(item1.location.pk, self.test_storage1.pk)

    def test_update_item_quantity_POST_no_login(self):
        """Test update item quantity returns 302 without login."""
        self.assertEqual(self.item1.quantity, 1)
        response = self.client.post(self.update_item_quantity_url, {"item_id": self.item1.pk, "new_qty": 5})
        self.assertEquals(response.status_code, 302)
        item1 = Item.objects.get(pk=self.item1.pk)
        self.assertEqual(item1.quantity, 1)

    def test_update_item_quantity_GET_no_login(self):
        """Test update item quantity returns 302 without login."""
        self.assertEqual(self.item1.quantity, 1)
        response = self.client.get(self.update_item_quantity_url, {"item_id": self.item1.pk, "new_qty": 5})
        self.assertEquals(response.status_code, 302)
        item1 = Item.objects.get(pk=self.item1.pk)
        self.assertEqual(item1.quantity, 1)

    def test_item_index_no_login(self):
        """Test item_index returns 302 without login."""
        response = self.client.get(self.item_index_url)
        self.assertEquals(response.status_code, 302)

    def test_storage_detail_no_login(self):
        """Test storage_detail returns 302 without login."""
        response = self.client.get(self.storage_detail_url)
        self.assertEquals(response.status_code, 302)

    def test_storage_index_no_login(self):
        """Test storage_index returns 302 without login."""
        response = self.client.get(self.storage_index_url)
        self.assertEquals(response.status_code, 302)

    def test_new_item_no_login(self):
        """Test new_item returns 302 without login."""
        response = self.client.get(self.new_item_url)
        self.assertEquals(response.status_code, 302)

    def test_new_item_from_storage_no_login(self):
        """Test new_item_from_storage returns 302 without login."""
        response = self.client.get(self.new_item_from_storage_url)
        self.assertEquals(response.status_code, 302)

    def test_new_storage_no_login(self):
        """Test new_storage returns 302 without login."""
        response = self.client.get(self.new_storage_url)
        self.assertEquals(response.status_code, 302)

    def test_new_storage_from_room_no_login(self):
        """Test new_storage_from_room returns 302 without login."""
        response = self.client.get(self.new_storage_from_room_url)
        self.assertEquals(response.status_code, 302)

    def test_search_no_login(self):
        """Test search returns 302 without login."""
        response = self.client.get(self.search_results_url, {'q': "Test Item"})
        self.assertEquals(response.status_code, 302)

    def test_reorder_list_no_login(self):
        """Test reorder_list returns 302 without login."""
        response = self.client.get(self.reorder_url)
        self.assertEquals(response.status_code, 302)

    def test_missing_items_no_login(self):
        """Test missing_items returns 302 without login."""
        response = self.client.get(self.missing_items_url)
        self.assertEquals(response.status_code, 302)
