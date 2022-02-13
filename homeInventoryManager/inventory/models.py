from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


CONDITION_CHOICES = (
    ("Good", "Good"),
    ("Fair", "Fair"),
    ("Poor", "Poor"),
    ("Broken", "Broken"),
    ("Unknown", "Unknown"),
)

DOCTYPE_CHOICES = (
    ("User Manual", "User Manual"),
    ("Receipt", "Receipt"),
    ("Warranty information", "Warranty information"),
    ("Other", "Other"),
)
STORAGETYPE_CHOICES = (
    ("Shelf", "Shelf"),
    ("Drawer", "Drawer"),
    ("Cabinet", "Cabinet"),
    ("Box", "Box"),

)


class CustomUser(AbstractUser):
    def __str__(self):
        """Return string representation of object."""
        if self.first_name:

            return f"{self.first_name} {self.last_name}"
        else:
            return self.username


class Room(models.Model):
    class Meta:
        """Metadata."""

        ordering = ("name",)
    name = models.CharField(max_length=200)

    def __str__(self):
        """Return string representation of object."""
        return self.name


class Storage(models.Model):
    class Meta:
        """Metadata."""

        ordering = ("name",)

    name = models.CharField(max_length=200)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, blank=True, null=True, help_text='Short description of the location. Ex: "office supplies", "model trains", "small electronic parts"')
    type = models.CharField(max_length=30, choices=STORAGETYPE_CHOICES, default="----", blank=True, null=True)

    def __str__(self):
        """Return string representation of object."""
        return "{} -> {}".format(self.room.name, self.name)

    def __repr__(self):
        """Return representation of object."""
        return "{} -> {}".format(self.room.name, self.name)

    def get_queryset_common_items(self):
        """Return queryset of 5 items with the most quantity in container."""
        print("hello")
        return self.Item.objects.all()

    def get_queryset(self):
        """Return queryset of all objects, ordered by name."""
        return self.objects.all().order_by(self.name)


class Item(models.Model):
    name = models.CharField(max_length=200)
    location = models.ForeignKey(Storage, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    par_value = models.IntegerField(default=0)
    purchase_date = models.DateField(auto_now=False, blank=True, null=True)
    purchase_price = models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)
    warranty_expire_date = models.DateField(auto_now=False, blank=True, null=True)
    model_number = models.CharField(max_length=50, blank=True, null=True)
    serial_number = models.CharField(max_length=200, blank=True, null=True)
    asset_tag = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default="Good")
    last_seen = models.DateTimeField(auto_now=False, blank=True, null=True)
    missing = models.BooleanField(default=False)
    missing_since = models.DateTimeField(auto_now=False, blank=True, null=True)

    def __str__(self):
        """Return string representation of object."""
        return self.name

    def confirm_location(self):
        """Update item to show it has been returned to it"s assigned location."""
        self.last_seen = timezone.now()
        self.missing_since = None
        self.missing = False
        self.save()

    def report_missing(self):
        """Mark item as missing."""
        self.missing = True
        self.missing_since = timezone.now()
        self.save()

    def update_location(self, new_loc_pk):
        """Update item location."""
        self.missing = False
        self.last_seen = timezone.now()
        # print("new location ", new_loc_pk)
        self.location = Storage.objects.get(pk=new_loc_pk)
        self.save()

    def update_quantity(self, new_qty):
        """Update item quantity."""
        self.quantity = new_qty
        self.save()


class Document(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    file = models.FileField(upload_to="docs/", blank=True, null=True)
    type = models.CharField(max_length=200, choices=DOCTYPE_CHOICES, default="User Manual")
    displayName = models.CharField("Display Name", max_length=200, blank=True, null=True)

    def __str__(self):
        """Return string representation of object."""
        return self.type
