#!/bin/bash

logname=$(logname)
path=$(pwd)

if grep -q "$path/Temperature.sh" "/var/spool/cron/crontabs/$logname"
then
    echo "Skript ist schon vorhanden!"
else 
    chmod -v 777 "/var/spool/cron/crontabs/"
    chmod -v 777 "/var/spool/cron/crontabs/$logname"

    echo "*/5 * * * * $path/Temperature.sh" >> "/var/spool/cron/crontabs/$logname"

    chmod -v 600 "/var/spool/cron/crontabs/$logname"
    chmod -v 730 "/var/spool/cron/crontabs/"
fi