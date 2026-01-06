#!/bin/bash
# Deployment script for Hugging Face Spaces

echo "Hugging Face Spaces Deployment Script"
echo "====================================="

echo "Before running this script, make sure you have:"
echo "1. Created a Space on Hugging Face Hub"
echo "2. Set up your environment variables in the Space settings"
echo "3. Installed huggingface_hub: pip install huggingface_hub"
echo ""

read -p "Enter your Hugging Face username: " username
read -p "Enter your Space name: " space_name

echo "Creating deployment files..."

# Create the huggingface.yml configuration file
cat > huggingface.yml << EOF
runtime:
  cpu: 2
  memory: 8GiB
  accelerator: cpu
  concurrency: 1
  timeout: 100
secrets:
  - COHERE_API_KEY
  - QDRANT_URL
  - QDRANT_API_KEY
  - NEON_DATABASE_URL
  - QDRANT_COLLECTION_NAME
EOF

echo "Deployment files created successfully!"
echo ""
echo "To deploy your application, run:"
echo "huggingface-cli upload $username/$space_name ./* --repo-type space"
echo ""
echo "Or, if you prefer to use Git:"
echo "1. Clone your Space repository: git clone https://huggingface.co/spaces/$username/$space_name"
echo "2. Copy all files from this directory to the cloned repository"
echo "3. git add ."
echo "4. git commit -m 'Initial deployment'"
echo "5. git push origin main"
echo ""
echo "Remember to set these environment variables in your Space settings:"
echo "- COHERE_API_KEY"
echo "- QDRANT_URL"
echo "- QDRANT_API_KEY"
echo "- NEON_DATABASE_URL"
echo "- QDRANT_COLLECTION_NAME (optional, defaults to 'book_embeddings')"