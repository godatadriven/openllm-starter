#!/bin/bash

IDLE_TIME=3600  # 1 hour in seconds
THRESHOLD=5     # CPU usage threshold in percentage

while true; do
  sleep 60  # Check every minute
  CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1"%"}' | awk -F. '{print $1}')
  
  if [ "$CPU_USAGE" -le "$THRESHOLD" ]; then
    IDLE_TIME=$((IDLE_TIME - 60))
  else
    IDLE_TIME=3600
  fi

  if [ "$IDLE_TIME" -le 0 ]; then
    sudo shutdown -h now
    break
  fi
done