#!/usr/bin/env bash

docker run --rm --name=test-container -p 8000:80 "$@" pylint /app/app.py

docker run --rm --name=test-container -p 8000:80 "$@" pylint /app/predict.py
