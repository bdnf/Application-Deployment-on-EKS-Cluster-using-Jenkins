#!/usr/bin/env bash

exclude_linter_rules="--disable=R1705"

docker run --rm --name=test-container -p 8000:80 "$@" pylint $exclude_linter_rules \
                                                      /app/app.py

docker run --rm --name=test-container -p 8000:80 "$@" pylint $exclude_linter_rules \
                                                      /app/predict.py
