#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Flush the database (this will delete all data and re-create the database)
python manage.py flush --no-input

# Apply any outstanding database migrations
python manage.py migrate

python manage.py makemigrations

# Convert static asset files
python manage.py collectstatic --no-input



