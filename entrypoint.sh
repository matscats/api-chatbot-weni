#!/bin/sh

echo 'Running commands'

cd app/
python manage.py populate_default_channels
python manage.py setup_telegram_webhook