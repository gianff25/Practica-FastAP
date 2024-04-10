#!/bin/bash

# Instalar dependencias nuevas
pip install -r ./requirements.project.txt

# run fastapi server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload # --workers $UVICORN_WORKERS
