#!/bin/bash

# Script to update the publish workflow when a new version gets added
rm -f .github/workflows/publish_*.yml > /dev/null
python3 .github/workflows/scripts/workflow_gen.py