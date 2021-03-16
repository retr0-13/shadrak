#!/usr/bin/env bash
#set -x

# https://softwareengineering.stackexchange.com/questions/279207/how-deeply-can-a-json-object-be-nested

char=$(pwgen 1 1)

printf '{'

#slow but different key each time
#for i in $(seq 0 ${1}); do printf "\"$(pwgen 1 1)\":{"; done
printf "%${1}s" | sed "s/ /\"${char}\":{/g"

printf "%${1}s" | sed 's/ /}/g'

printf '}'
