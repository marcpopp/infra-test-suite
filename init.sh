#!/bin/bash

set -e

# Add binaries of python libraries installed by local user
PATH=$PATH:$HOME/.local/bin

# Get the right name of the python package manager
PIP=pip2
if [ "$( command -v $PIP )" == "" ]; then
    PIP=pip
fi

# Change into test root as working directory
cd "$(dirname "$0")"

$PIP install --requirement requirements.txt --user

exit 0
