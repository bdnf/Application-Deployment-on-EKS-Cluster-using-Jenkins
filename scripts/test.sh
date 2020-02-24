#!/usr/bin/env bash

exclude_linter_rules="--disable=C0103 \
                        --disable=C0321 \
                        --disable=W1201 \
                        --disable=R1705 \
                        --disable=E1101 \
                        --disable=W0614 \
                        --disable=W0401 \
                        --disable=W0221 \
                        --disable=R1705"

docker run --rm --name=test-container -p 8000:80 "$@" pylint $exclude_linter_rules \
                                                      /app/app.py

docker run --rm --name=test-container -p 8000:80 "$@" pylint $exclude_linter_rules \
                                                      /app/predict.py
