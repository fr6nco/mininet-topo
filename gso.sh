#!/bin/bash

interfaces="eth1 eth2 eth3 eth4 eth5 eth6"

for i in $interfaces; do
	ethtool -K $i gso off
	ethtool -K $i gro off
	ethtool -K $i tso off
done

