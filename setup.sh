#!/bin/sh
set -e
inst() {
    echo $(tput bold 2>/dev/null || printf '')"==> go get $1"$(tput sgr0 2>/dev/null || printf '')
    go get "$1"
}
cat packages.txt | while read pkg; do inst "$pkg"; done
