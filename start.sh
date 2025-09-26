#!/bin/bash

echo "🕸️  Starting Darkwebsearch Prototype..."
echo "========================================"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if Docker Compose is available
if ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available. Please install Docker Compose plugin."
    exit 1
fi

echo "📋 Building and starting all services..."
echo ""

# Start services
docker compose up --build -d

echo ""
echo "⏳ Waiting for services to initialize..."
sleep 10

echo ""
echo "🎉 Darkwebsearch Prototype is starting up!"
echo ""
echo "📍 Service URLs:"
echo "   🔍 SvelteKit GUI:     http://localhost:3000"
echo "   🎛️  Manager Dashboard: http://localhost:5000"
echo "   🕷️  Crawler Service:   http://localhost:5001"
echo "   📊 Analysis Service:  http://localhost:5002"
echo ""
echo "💡 Usage Tips:"
echo "   • Wait ~30 seconds for MySQL to fully initialize"
echo "   • Visit the Manager Dashboard to monitor services"
echo "   • Start a crawl to populate search data"
echo "   • Use 'docker compose logs' to view service logs"
echo ""
echo "🛑 To stop all services:"
echo "   docker compose down"
echo ""
echo "Happy searching! 🚀"