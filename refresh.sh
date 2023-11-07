#!/bin/bash
python refresh.py
git add items.csv
git commit -m "update"
git push
