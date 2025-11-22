#!/usr/bin/env bash
# Render build script for backend

# Exit on error
set -e

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt

echo "Backend build completed successfully!"
