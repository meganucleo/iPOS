#!/bin/bash
#Bash wrapper for java encrypt
#Leon Ramos
#2015

PATH=$1
USR=$2
PASS=$3
JAVA=/usr/bin/java
export CLASSPATH=$1
$JAVA utils/encrypt $USR $PASS
