#!/bin/bash
set -e

echo "🚀 Deploying AccessRating Backend to Production..."

# Check if .env.prod exists
if [ ! -f ".env.prod" ]; then
    echo "❌ .env.prod file not found!"
    echo "Please copy .env.prod.example to .env.prod and configure it."
    exit 1
fi

# Check if domain is configured in Caddyfile
if grep -q "your-domain.com" caddy/Caddyfile; then
    echo "❌ Domain not configured in Caddyfile!"
    echo "Please run: ./scripts/setup-ssl.sh yourdomain.com"
    exit 1
fi

echo "📦 Building Docker images..."
docker-compose -f docker/docker-compose.prod.yml build

echo "🗄️ Starting database and cache..."
docker-compose -f docker/docker-compose.prod.yml up -d db redis

echo "⏳ Waiting for database to be ready..."
sleep 10

echo "🔄 Running database migrations..."
docker-compose -f docker/docker-compose.prod.yml run --rm web python manage.py migrate --settings=accessibility_api.prod_settings

echo "📁 Collecting static files..."
docker-compose -f docker/docker-compose.prod.yml run --rm web python manage.py collectstatic --noinput --settings=accessibility_api.prod_settings

echo "🔧 Starting all services..."
docker-compose -f docker/docker-compose.prod.yml up -d

echo "🏥 Waiting for services to be healthy..."
sleep 15

# Check if health endpoint is working
DOMAIN=$(grep -o '[a-zA-Z0-9.-]*\.[a-zA-Z]{2,}' caddy/Caddyfile | head -1)
if curl -f -s "https://$DOMAIN/health/" > /dev/null; then
    echo "✅ Health check passed!"
else
    echo "⚠️ Health check failed - check logs with: make prod-logs"
fi

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "📍 Your backend is available at:"
echo "   🔗 https://$DOMAIN/"
echo "   🔗 https://$DOMAIN/admin/"
echo "   🔗 https://$DOMAIN/api/v1/"
echo "   ❤️ https://$DOMAIN/health/"
echo ""
echo "📊 Monitor with:"
echo "   📋 make prod-logs"
echo "   🔍 docker-compose -f docker-compose.prod.yml ps"
echo ""
echo "⚠️ Don't forget to create a superuser:"
echo "   🧑‍💼 make prod-shell"
