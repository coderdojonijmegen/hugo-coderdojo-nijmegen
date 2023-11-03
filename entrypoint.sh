#!/usr/bin/env bash

set -e

pushd /site/
PYTHONPATH=/site/src/ python3 -u /site/src/deploy.py
