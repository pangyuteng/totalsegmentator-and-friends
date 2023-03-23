#!/bin/bash
echo $@

cd /mnt/hd1/github/totalsegmentator-and-friends/nn/totalseg2023
python train.py
