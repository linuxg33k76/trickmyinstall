#!/usr/bin/env bash

# This script is used to create SSH keys

# Check if SSH keys already exist

if [ -f ~/.ssh/id*.pub ]; then
    echo "SSH keys already exist."
else
    echo "Generating SSH keys..."
    ssh-keygen
fi

exit 0