#!/bin/bash

logname=$(logname)
echo "*/5 * * * * $(pwd)/Temperature.sh" >> "/var/spool/cron/crontabs/$logname"