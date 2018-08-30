#!/bin/sh

set -e

sed -i 's/python27/python36/g' ~/.bashrc
sudo alternatives --set python /usr/bin/python3.6

