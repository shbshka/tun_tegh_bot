#!/bin/bash
cd /home/shbshka/tun-tegh-bot &&\
source ./.venv/bin/activate &&\
nohup python3 -u main.py >> bot_log.txt &
