#!/bin/bash

docker-compose run \
  -e DJANGO_SETTINGS_MODULE=home.settings.testing \
  --no-deps --rm webhi py.test;
