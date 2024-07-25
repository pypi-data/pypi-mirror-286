#!/bin/bash

# clear out the dist folder
rm -rf dist/*

# Build the Docker image
podman build -t testsmartenough .

# Run the Docker container with environment variables passed from the host
podman run --rm \
  -e OPENAI_API_KEY="$OPENAI_API_KEY" \
  -e ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
  -e MISTRAL_API_KEY="$MISTRAL_API_KEY" \
  -e GOOGLE_API_KEY="$GOOGLE_API_KEY" \
  -e OPENROUTER_API_KEY="$OPENROUTER_API_KEY" \
  testsmartenough
