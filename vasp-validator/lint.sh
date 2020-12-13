#!/usr/bin/env sh

echo "> Running Black"
pipenv run black libra tests
echo

echo "> Running flake8"
pipenv run flake8 . 

