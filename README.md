Status as of June 29, 2022: There are multiple issues. Migrations are not being correctly applied in the docker image. I do not currently have time to investigate. This was the first project I made with django, and I haven't really done much with it since. 

# Home Inventory
## About
This project grew out of some needs I had in my home. I have many small parts for my various electronics projects, often scattered across many boxes/bins. My overall goal was to spend less time searching boxes and trying to remember "where did I put that widget 3 years ago?".

## Screenshots

Desktop version
![Desktop version](https://github.com/haicenhacks/homeInventory/blob/main/inventory_item_detail_desktop.png?raw=true)

Mobile version
![Mobile version](https://github.com/haicenhacks/homeInventory/blob/main/inventory_item_detail_mobile.png?raw=true)
## The data models

### Rooms
Rooms are locations like "Bedroom", "Office", or "Storage Shed". Each room contains one or more **Storage** objects.

### Storages
Storage objects are containers or areas in which items are stores.

Fields
* Name - a (preferably) unique short identifier
  * examples: "D1", "C1", "S1"; (short code for "Drawer 1", "Cabinet 1", "Shelf 1", respectively)
* Description (optional) - a friendly name, preferably one that describes what types of items should be stored in the location
  * examples: "office supplies", "model trains", "small electronic parts"
* Type (optional) - container type. this can be customized in `inventory/models.py`

Additionally, when listing storage containers in each room, the 5 items with the highest quantity are shown as a list.

### Items
Items are any objects that exist in a **Storage**

Fields:

* name - the name displayed
* location - the **Storage** it is contained in
* quantity
  * optional, default=1
* par_value - the minimum quantity of the object when it should be reordered
  * optional, default=0
* purchase_date, optional
* purchase_price, optional
* warranty_expire_date, optional, the date the warranty expires
* model_number, optional
* serial_number, optional
* asset_tag (optional) - a tag or other identifier that could be printed on a barcode label
* notes, optional
* image, optional, only one image per item is currently supported. Additional images could be stored in the item documents
* condition - the condition of the item
* last_seen - the last time the item was seen. only visible in the site admin settings
* missing - indicates that the item is missing
* missing_since - the time the item was reported missing

# The workflow

Since rooms are typically fixed and do not require frequent user modification, these must be defined using the admin interface. This must be completed before defining any items or storage containers.

Each **Storage** has a detail view that lists all items that are assigned to that location. By clicking the "missing" or "present" buttons, it will mark each item as present or missing. Items that have been marked missing with be listed on the "missing items" page.
For example: you have moved an object from it's assigned location and forgot to put it back. On a later date, you need that item, and cannot find it in it's location, the item should be marked missing. Later, if you find it while cleaning or reorganizing, the item can be quickly found on the missing item page, and marked as present or change the assigned location.

Documents related to the item, such as warranty cards, user manuals, or additional images can be uploaded and will be displayed on the item detail page.

Otherwise, it is basically just a database with all your stuff.

# Installation instructions

Like any django app, it requires a few things to be functional. The simplest way to get the app running is to use the docker compose file included.

`docker-compose up --build`

since this is something that I largely use in my home lab through a vpn, I do not have ssl enabled. To enable ssl, the nginx configuration needs to be modified to add

```
listen 443 ssl;
ssl_certificate /home/app/web/ssl_certs/fullchain1.pem;
ssl_certificate_key /home/app/web/ssl_certs/privkey1.pem;
```
and the location of your ssl certificates need to be added as a volume in the docker-compose file
```
      - /etc/letsencrypt/archive/your_site:/home/app/web/ssl_certs/
```

some example data is included. Comment out the relevant line in app/entrypoint.sh to avoid the import before running docker-compose.

A `superuser` account should be created, either by first building the images using `docker-compose`, or by using `django-admin` in the entrypoint.sh file using the syntax described in the [django documentation](https://docs.djangoproject.com/en/3.0/ref/django-admin/#django-admin-createsuperuser)

```django-admin createsuperuser --no-input --username=admin --email admin@example.com --password <some password>```

Finally, the docker environment variables need to be defined in homeInventory/project.env:
```
POSTGRES_USER=django
POSTGRES_PASSWORD=<password here>
POSTGRES_DB=project_db

DATABASE=postgres
DATABASE_HOST=postgresdb
DATABASE_PORT=5432
DOCKER=TRUE
```

This is used in the docker-compose build process to configure the password for the postgres database and in the django app for accessing the database
