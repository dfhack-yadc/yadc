#!/bin/sh
set -e
run=
opts=
while [ $# -gt 0 ]
do
    case "$1" in
        -r|--run) run=1
            ;;
        *) opts="$opts $1"
            ;;
    esac
    shift
done

if [ -n "$opts" ] && [ -z "$run" ]; then
    printf "runtime options specified but (-r|--run) not passed:\n%s\n" "$opts"
    exit 1
fi

run_cmd() {
    echo $(tput bold 2>/dev/null || printf '')"==> $@"$(tput sgr0 2>/dev/null || printf '')
    "$@"
}

cd $(dirname "$0")
run_cmd go-bindata-assetfs web/...
run_cmd go build -o build/yadc
if [ -n "$run" ]; then
    run_cmd ./build/yadc $opts || true
fi
