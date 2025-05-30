#!/bin/bash
apt-get update
apt-get install -y $(cat packages.txt)
pip install --upgrade pip
pip install -r requirements.txt