#!/usr/bin/env bash

docker build -t "$@" -f ./app/Dockerfile ./app
