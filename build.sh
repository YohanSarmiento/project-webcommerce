#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Apply any outstanding database migrations
python manage.py migrate

# Convert static asset files
python manage.py collectstatic --no-input

# Flush the database (this will delete all data and re-create the database)
python manage.py flush --no-input



