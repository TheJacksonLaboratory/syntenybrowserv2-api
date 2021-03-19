#!/bin/sh

if [ -z "$PRODUCTION" ] ; then
  echo "# System ------------"
  uname -a
  echo "# Storage -----------"
  lsblk
  echo "# CPU ---------------"
  lscpu
  echo "# -------------------"
  mascot
fi

exec "$@"