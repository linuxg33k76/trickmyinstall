#!/usr/bin/env bash

# Script to setup GPG for GitHub Commits
echo "This script will setup GPG for GitHub Commits."
echo ""


# Check if gpg is installed
if ! command -v gpg &> /dev/null; then
    echo "GPG is not installed. Attempting to install..."
    if [ "$(uname)" = "Darwin" ]; then
        brew install gpg
    elif [ "$(uname)" = "Linux" ]; then
        
        # Get package manager
        if command -v pacman &> /dev/null; then
            sudo pacman -S gpg
        elif command -v dnf &> /dev/null; then
            sudo dnf install gpg
        elif command -v apt &> /dev/null; then
            sudo apt install gpg
        else
            echo "Could not find package manager. Exiting."
            exit 1
        fi
    fi
fi

if ! command -v gpg &> /dev/null; then
    echo "GPG is not installed. Exiting."
    exit 1
fi

# Ask user for GPG key location
read -p "Enter your GPG private key location: " gpg_private_key

# Check if private key is present
echo "Checking for private key at ${gpg_private_key}\n"
if ! test -f "${gpg_private_key}"; then
    echo "Private key not found. Exiting."
    exit 1
fi

# Import GPG key
gpg --import "${gpg_private_key}"

# List secret keys
gpg --list-secret-keys --keyid-format=LONG

# Ask user for GPG key ID
read -p "Enter your GPG key ID: " gpg_key_id

# Set the key ID
git config --global user.signingkey "${gpg_key_id}"

# Enable signing for all commits
git config --global commit.gpgsign true

# Point Git to the GPG binary (crucial on macOS)
git config --global gpg.program $(which gpg)

echo ""
echo "GPG setup complete. Private keys have been imported and Git is configured to use them!"