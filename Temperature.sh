#!/bin/bash

temp="$(vcgencmd measure_temp | grep -oP '\d\d\.\d')"
mac="$(cat /sys/class/net/eth0/address)"

curl -X PUT h2948228.stratoserver.net -H 'Content-Type: application/json' -d '{"temperature":"'$temp'", "macAddress":"'$mac'"}'