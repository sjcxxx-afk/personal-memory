# Personal Memory Service - Build and Run Script
# This script builds and runs the personal memory service using Docker

Write-Host "🚀 Personal Memory Service - Build and Run Script" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# Check if Docker is running
Write-Host "🔍 Checking Docker status..." -ForegroundColor Yellow
try {
    docker info | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Build the Docker image
Write-Host "🔨 Building Docker image..." -ForegroundColor Yellow
docker build -t personal-memory .

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker build failed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker image built successfully" -ForegroundColor Green

# Stop existing container if running
Write-Host "🛑 Stopping existing container (if any)..." -ForegroundColor Yellow
docker stop personal-memory-service 2>$null
docker rm personal-memory-service 2>$null

# Run the container
Write-Host "🚀 Starting Personal Memory Service..." -ForegroundColor Yellow
docker-compose up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to start container" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Personal Memory Service started successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Service Information:" -ForegroundColor Cyan
Write-Host "   Container: personal-memory-service" -ForegroundColor White
Write-Host "   Status: Running in background" -ForegroundColor White
Write-Host ""
Write-Host "🔧 Useful Commands:" -ForegroundColor Cyan
Write-Host "   View logs: docker-compose logs -f" -ForegroundColor White
Write-Host "   Stop service: docker-compose down" -ForegroundColor White
Write-Host "   Restart: docker-compose restart" -ForegroundColor White
Write-Host ""
Write-Host "🎯 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Configure your AI client to connect to this service" -ForegroundColor White
Write-Host "   2. Use MCP tools to store and search facts" -ForegroundColor White
Write-Host "   3. Monitor logs for any issues" -ForegroundColor White
Write-Host ""
Write-Host "📖 For configuration details, see README.md" -ForegroundColor Yellow