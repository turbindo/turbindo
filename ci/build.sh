#!/usr/bin/env bash
rm -rf turbindo.egg-info dist .eggs __pycache__ build
python3 -m pip install ./
python3 setup.py sdist bdist_wheel
