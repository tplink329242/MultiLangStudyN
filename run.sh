#!/bin/sh

nohup python3 collect.py -s collect
nohup python3 collect.py -s clone
nohup python3 collect.py -s readme