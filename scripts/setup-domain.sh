#!/bin/bash
set -e

echo "🔧 Setting up Caddy with automatic HTTPS..."

# Check if domain is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <your-domain.com>"
    exit 1
fi

DOMAIN=$1

echo "Setting up Caddy for domain: $DOMAIN"

# Update Caddyfile with your domain
sed -i "s/your-domain.com/$DOMAIN/g" Caddyfile

echo "✅ Caddyfile configured!"
echo "Caddy will automatically obtain SSL certificates when you deploy."
echo "Make sure your domain DNS points to this server first!"
echo "Now run: ./scripts/deploy.sh"
