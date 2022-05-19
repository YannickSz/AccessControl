#!/bin/bash

logname=$(logname)
path=$(pwd)

if [ ! -e "/var/spool/cron/crontabs/$logname" ] ; then
    echo "" > "/var/spool/cron/crontabs/$logname"
fi

if grep -q "$path/Temperature.sh" "/var/spool/cron/crontabs/$logname"
then
    echo "Skript ist schon vorhanden!"
else
    chmod a+x "Temperature.sh"
    chmod -v 777 "/var/spool/cron/crontabs/"
    chmod -v 777 "/var/spool/cron/crontabs/$logname"

    echo "" >> "/var/spool/cron/crontabs/$logname"
    echo "*/5 * * * * $path/Temperature.sh" >> "/var/spool/cron/crontabs/$logname"
fi