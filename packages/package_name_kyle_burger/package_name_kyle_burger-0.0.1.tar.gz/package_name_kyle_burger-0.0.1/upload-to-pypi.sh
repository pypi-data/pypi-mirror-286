#!/usr/bin/env sh

# This script is used to upload the package to PyPI.
# It iterates through the dist directory and uploads all files to PyPI.
# It does not use twine. Instead, it uploads the files using the requests library.

# Usage: ./upload-to-pypi.sh

# Check if the dist directory exists
if [ ! -d "dist" ]; then
  echo "The dist directory does not exist. Run 'python setup.py sdist bdist_wheel' to create the dist directory."
  exit 1
fi

# Get the username and password from the user
echo "Enter your PyPI API key: "
read -r key

# Iterate through the files in the dist directory
for file in dist/*; do
  echo "Uploading $file to PyPI..."
  # Upload the file to PyPI
  response=$(curl -X POST -F "content=@$file" -u "__token__:$key" https://upload.pypi.org/legacy/)
  # Check if the upload was successful
  if echo "$response" | grep -q "400 Bad Request"; then
    echo "Upload failed. Check the error message above."
    exit 1
  else
    echo "Upload successful."
  fi
done