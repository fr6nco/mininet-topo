#!/bin/bash

rsync -avz -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" --progress --exclude '.git' ./* $1:~/$2
