#!/bin/bash
result=$(abduco -l | sed '1d'|dmenu)
if [ -z "$result" ];then 
  exit 
fi
id=$(echo "$result"| sed -E 's/.*[[:blank:]]([^[:blank:]]+)$/\1/')
kitty -1 bash -c "abduco -A $id bash"

