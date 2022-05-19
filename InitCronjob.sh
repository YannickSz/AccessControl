#!/bin/bash

logname=$(logname)

chmod -v 777 "/var/spool/cron/crontabs/"
chmod -v 777 "/var/spool/cron/crontabs/$logname"

echo "*/5 * * * * $(pwd)/Temperature.sh" >> "/var/spool/cron/crontabs/$logname"

chmod -v 600 "/var/spool/cron/crontabs/$logname"
chmod -v 730 "/var/spool/cron/crontabs/"
