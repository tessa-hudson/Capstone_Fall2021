#!/bin/sh
. venv/bin/activate
pip install -r requirements.txt
python api/app.py
