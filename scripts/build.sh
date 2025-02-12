#!/usr/bin/env bash

rm -rf build
rm -rf dist
rm -rf md_tangle.egg-info

python setup.py bdist_wheel
python3 setup.py bdist_wheel
