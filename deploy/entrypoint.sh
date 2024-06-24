#!/bin/sh

# NOTE: this script is run on container startup; it can be used 
# for any os operations you would like to run prior to starting the application: 
# e.g. collecting static files, applying database migrations, etc.

if [ -z "$PRODUCTION" ] ; then
  echo "# System ------------"
  uname -a
  echo "# Storage -----------"
  lsblk
  echo "# CPU ---------------"
  lscpu
fi

exec "$@"