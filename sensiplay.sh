#!/bin/bash
set -e
SCRIPTFILE=$(readlink -f "$0")
SCRIPTDIR=$(dirname "$SCRIPTFILE")

python3 $SCRIPTDIR/build_roles_from_sensible.py
ansible-playbook "$@"