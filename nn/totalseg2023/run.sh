#!/bin/bash
echo $@

cd /cvibraid/cvib2/apps/personal/pteng/nn/totalseg2023
python train.py
