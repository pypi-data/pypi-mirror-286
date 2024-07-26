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
  case $file in 
    *.tar.gz) filetype="sdist" ;;
    *.whl) filetype="bdist_wheel" ;;
    *) echo "Unsupported file type: $file"; exit 1 ;;
  esac
  if [ "$filetype" = "sdist" ]; then
    tar -xvzf "$file" -C /tmp/
    metadata_path="/tmp/$(basename "$file" .tar.gz)/PKG-INFO"
  else
    unzip -o "$file" -d "/tmp/$(basename "$file" .whl)"
    metadata_path="/tmp/$(basename "$file" .whl)/$(basename "$file" .whl | sed 's/-py3-none-any.*//').dist-info/METADATA"
  fi

  md5=$(md5sum "$file" | cut -d " " -f 1)

  description=""
  description_mode=0

  curl_command="curl -X POST -F \"content=@$file\" -F \":action=file_upload\" -F \"protocol_version=1\" -u \"__token__:$key\" -F \"md5_digest=$md5\" -F \"filetype=$filetype\""

  # Unzip file

  while IFS= read -r line; do
    # Check if the line contains "Description-Content-Type"
    if echo "$line" | grep -q '^Description-Content-Type'; then
        form_key="description-content-type"
        value=$(echo "$line" | cut -d ':' -f 2- | xargs)
        form_data="$form_data -F \"$form_key=$value\""
        # From the next line onwards, treat all lines as part of the description
        description_mode=1
        continue
    fi
 
    # If in description mode, append lines to the description
    if [ $description_mode -eq 1 ]; then
        description=$(printf "%s\n%s" "$description" "$line")
    elif echo "$line" | grep -q '^Requires-Python'; then
        form_key="pyversion"
        if [ "$filetype" = "sdist" ]; then
            value="source"
        else
            value=$(echo "$line" | cut -d ':' -f 2- | xargs)
        fi
        curl_command="$curl_command -F \"$form_key=$value\""
        continue
    else
        # Parse the form_key and value
        form_key=$(echo "$line" | cut -d ':' -f 1 | xargs | tr '[:upper:]' '[:lower:]' | tr '-' '_')
        value=$(echo "$line" | cut -d ':' -f 2- | xargs)
        echo "$form_key: $value"
        curl_command="$curl_command -F \"$form_key=$value\""
    fi
  done < "$metadata_path"

  encoded_description=$(printf '%s' "$description" | sed 's/[&/\]/\\&/g; s/ /\%20/g; s/\n/\\n/g')
  curl_command="$curl_command -F \"description=$encoded_description\" https://upload.pypi.org/legacy/"

  echo $curl_command

  response=$(eval $curl_command)



  # Upload the file to PyPI
#   response=$(curl -X POST -F "content=@$file" -F ":action=file_upload" -F "protocol_version=1" -u "__token__:$key" -F "md5_digest=$md5" -F "filetype=$filetype" -F "description=$description" $form_data https://upload.pypi.org/legacy/)
  # Check if the upload was successful
  if echo "$response" | grep -q "400"; then
    echo "$response"
    echo "Upload failed. Check the error message above."
    exit 1
  else
    echo "Upload successful."
    echo "$response"
  fi
done