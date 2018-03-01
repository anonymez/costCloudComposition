#!/usr/bin/env bash

prefix="fitting"
source ../costenv/bin/activate


for WINDOW in 1 2 3 4:
do
    echo "running Window $WINDOW"
    echo "WINDOW=$WINDOW">window.py
    for folder in datasets/*
    do
        newfolder=`echo $folder|sed -e 's/datasets\///g'|sed -e 's/.py//g'`
        mkdir -p "$prefix/$newfolder"
        cp $folder ./requests.py
        python test.py > "$prefix/$newfolder/$WINDOW.txt"
        cat "$prefix/$newfolder/$WINDOW.txt"|grep "TOTAL COST" |sed -e 's/TOTAL COST: //g' |sed -e 's/\./,/g'>"$prefix/$newfolder/cost$WINDOW.txt"
    done
done
