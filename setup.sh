#!/bin/bash

python -m venv /rinha-backend-2025-venv
export PATH="/rinha-backend-2025-venv/bin:$PATH"

source /rinha-backend-2025-venv/bin/activate

pip install -q --upgrade pip setuptools
pip install -q -r requirements.txt

python setup/main.py