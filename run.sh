#!/bin/bash

set -e

# Help
usage() {
   echo "Usage: $0 <ansible_inventory> [testfile ...]"
   exit 1
}

# Change into test root as working directory
cd "$(dirname "$0")"

# Add binaries of python libraries installed by local user
PATH=$HOME/.local/bin:$PATH
# Preset the number of forks to use
FORKS="-n 9"

# Parse Arguments - First argument has to be the inventory
INVENTORY=$1
shift
if [ "$INVENTORY" == "" ] || [ "$INVENTORY" == "--help" ] || [ ! -d "$INVENTORY" ]; then
    usage
fi

# Parse Arguments - Optional test files
PATTERN="$@"
if [ "$PATTERN" == "" ]; then
    PATTERN="tests/*/*.py"
else
    # Disable forks and output debug data, if explicit test files are given
    FORKS="--capture=no -v"
fi

# Cleanup old compiled versions and caches
find . -name "__pycache__" -o -name "*.pvc" -exec rm -r {} \;

# for the testHelpers
export PYTHONPATH=.
# Vault key for ansible
export ANSIBLE_VAULT_PASSWORD_FILE=${ANSIBLE_VAULT_PASSWORD_FILE:-'/etc/ansible/ansible_vault'}

# Start the tests
cmd="py.test --connection=ansible --ansible-inventory=$INVENTORY $FORKS -v --junitxml results.xml $PATTERN"
echo $cmd
exec $cmd

exit 0
