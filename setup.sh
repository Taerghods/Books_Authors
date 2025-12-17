#!/bin/bash

# تشخیص دستور مناسب (docker-compose یا docker compose)
if docker compose version > /dev/null 2>&1; then
    DOCKER_CMD="docker compose"
elif docker-compose version > /dev/null 2>&1; then
    DOCKER_CMD="docker-compose"
else
    echo "❌ Error: Docker Compose is not installed!"
    exit 1
fi

echo "✅ Using command: $DOCKER_CMD"

# ۱. توقف کانتینرهای قدیمی
echo "🚀 Stopping old containers..."
$DOCKER_CMD down

# ۲. بیلد کردن و بالا آوردن سیستم
echo "🏗️ Building and starting the system..."
$DOCKER_CMD up --build -d

# ۳. مقیاس‌دهی
echo "📈 Scaling the web service to 3 instances..."
$DOCKER_CMD up -d --scale web=3

echo "✅ System is up and running!"
docker ps