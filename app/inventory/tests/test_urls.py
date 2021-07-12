# import datetime

from django.test import TestCase
# from django.utils import timezone
from django.urls import reverse, resolve

from inventory.models import Room, Storage, Item, CustomUser
# class TestURLS(TestCase):


class testURLs(TestCase):
    def setUp(self):
        """Test setup."""
        self.user = CustomUser.objects.create_user(email='normal@user.com', username="testuser", password='foo')
        self.staff_user = CustomUser.objects.create_user(email='staff@user.com', username="staffuser", password='foo', is_staff=True)
        self.test_room = Room.objects.create(name="test room")
        self.test_storage1 = Storage.objects.create(name="test container1", room=self.test_room)
        self.test_storage2 = Storage.objects.create(name="test container2", room=self.test_room)
        # print(self.test_storage1.pk)
        self.item1 = Item(name="Test Item #1", location=self.test_storage1, quantity=1,
                          par_value=1, purchase_date="2021-06-01",
                          asset_tag="001", notes="some notes about item 1",
                          image=None, condition="Good",
                          model_number="A427", serial_number="551", warranty_expire_date=None,
                          pk=1
                          )

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

    def test_empty(self):
        """Test empty url resolves."""
        assert resolve(self.index_url).view_name == "inventory:index"

    def test_all_item_url(self):
        """Test all/ resolves."""
        assert resolve(self.all_items_url).view_name == "inventory:all_items"

    def test_room_detail(self):
        """Test room list resolves."""
        assert resolve(self.room_detail_url).view_name == "inventory:room_detail"

    def test_item_detail(self):
        """Test item detail resolves."""
        assert resolve(self.item_detail_url).view_name == "inventory:item_detail"

    def test_item_edit(self):
        """Test item edit resolves."""
        assert resolve(self.item_edit_url).view_name == "inventory:item_edit"

    def test_confirm_item_location(self):
        """Test vonfirm item location resolves."""
        assert resolve(self.confirm_item_location_url).view_name == "inventory:confirm_item_location"

    def test_report_item_missing(self):
        """Test report item missing resolves."""
        assert resolve(self.report_item_missing_url).view_name == "inventory:report_item_missing"

    def test_update_item_location(self):
        """Test update item location resolves."""
        assert resolve(self.update_item_location_url).view_name == "inventory:update_item_location"

    def test_update_item_quantity(self):
        """Test update item quantity resolves."""
        assert resolve(self.update_item_quantity_url).view_name == "inventory:update_item_quantity"

    def test_item_index(self):
        """Test item_index resolves."""
        assert resolve(self.item_index_url).view_name == "inventory:item_index"

    def test_storage_detail(self):
        """Test storage_detail resolves."""
        assert resolve(self.storage_detail_url).view_name == "inventory:storage_detail"

    def test_storage_index(self):
        """Test storage_index resolves."""
        assert resolve(self.storage_index_url).view_name == "inventory:storage_index"

    def test_new_item(self):
        """Test new_item resolves."""
        assert resolve(self.new_item_url).view_name == "inventory:new_item"

    def test_new_item_from_storage(self):
        """Test new_item_from_storage resolves."""
        assert resolve(self.new_item_from_storage_url).view_name == "inventory:new_item_from_storage"

    def test_new_storage(self):
        """Test new_storage resolves."""
        assert resolve(self.new_storage_url).view_name == "inventory:new_storage"

    def test_new_storage_from_room(self):
        """Test new_storage_from_room resolves."""
        assert resolve(self.new_storage_from_room_url).view_name == "inventory:new_storage_from_room"

    def test_search(self):
        """Test search resolves."""
        assert resolve(self.search_results_url).view_name == "inventory:search_results"

    def test_reorder_list(self):
        """Test reorder_list resolves."""
        assert resolve(self.reorder_url).view_name == "inventory:reorder_list"

    def test_missing_items(self):
        """Test missing_items resolves."""
        assert resolve(self.missing_items_url).view_name == "inventory:missing_list"
