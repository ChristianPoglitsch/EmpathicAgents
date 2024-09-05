#!/bin/sh

FILE_URL="https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml"
FILE_URL2="https://raw.githubusercontent.com/openai/openai-python/main/api.md"


DESTINATION_PATH="openapi.yaml"
DESTINATION_PATH2="openai_python_client_api.md"

curl -o $DESTINATION_PATH $FILE_URL
curl -o $DESTINATION_PATH2 $FILE_URL2