#!/bin/bash


while true;
do
	sleep 0.1
	curl http://cdn.example.com:8082/
	if [ $? -ne 0 ]; then
		break;
	fi
done
