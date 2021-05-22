#!/bin/bash

BMV2_PATH=../bmv2
P4C_BM_PATH=../p4c-bmv2
P4C_BM_SCRIPT=$P4C_BM_PATH/p4c_bm/__main__.py
SWITCH_PATH=$BMV2_PATH/targets/simple_switch/simple_switch
CLI_PATH=$BMV2_PATH/targets/simple_switch/sswitch_CLI

$P4C_BM_SCRIPT ../p4src/netcache.p4 --json netcache.json
sudo $SWITCH_PATH >/dev/null 2>&1
sudo PYTHONPATH=$PYTHONPATH:$BMV2_PATH/mininet/ python topo.py \
    --behavioral-exe $SWITCH_PATH \
    --json netcache.json \
    --cli $CLI_PATH
