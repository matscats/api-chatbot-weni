#!/bin/sh
set -e

echo 'Running commands'
cd app/

echo 'Creating default channels'
python manage.py populate_default_channels

echo 'Setup for telegram webhook'
python manage.py setup_telegram_webhook

echo "Executing migrations"
python manage.py migrate