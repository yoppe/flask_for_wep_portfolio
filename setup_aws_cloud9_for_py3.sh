#!/bin/sh

set -e

sed -i 's/alias python=python27//g' ~/.bashrc
sudo alternatives --set python /usr/bin/python3.6

