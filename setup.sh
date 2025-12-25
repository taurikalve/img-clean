#!/bin/bash

# Get the directory where this script is located
DIR=$(dirname "$(realpath "$0")")

# 1. Make the script executable (No sudo needed if you own the file)
chmod +x "$DIR/img_clean.py"

# 2. Setup Python Environment
if [ ! -d "$DIR/.venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$DIR/.venv"
    
    echo "Installing dependencies..."
    "$DIR/.venv/bin/pip" install --upgrade pip
    "$DIR/.venv/bin/pip" install -r "$DIR/requirements.txt"
else
    echo "Virtual environment already exists."
fi

# 3. Add Alias to .bashrc (only if it's not already there)
ALIAS_CMD="alias cleanimg='\"$DIR/.venv/bin/python\" \"$DIR/img_clean.py\"'"
RC_FILE="$HOME/.bashrc"

if grep -Fxq "$ALIAS_CMD" "$RC_FILE"; then
    echo "Alias 'cleanimg' already exists in $RC_FILE"
else
    echo "Adding alias 'cleanimg' to $RC_FILE..."
    echo "$ALIAS_CMD" >> "$RC_FILE"
    echo "Done! Run 'source $RC_FILE' or restart your terminal to use the command."
fi