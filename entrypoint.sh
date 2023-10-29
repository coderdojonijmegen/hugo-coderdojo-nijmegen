#!/usr/bin/env bash

set -e

pushd /site/
PYTHONPATH=/src/ python3 -u /src/deploy.py
