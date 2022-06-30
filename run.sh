#!/bin/sh
nohup python3 collect.py -s collect > full.log 2>&1 &
nohup python3 collect.py -s clone > full.log 2>&1 &
nohup python3 collect.py -s readme > full.log 2>&1 &
