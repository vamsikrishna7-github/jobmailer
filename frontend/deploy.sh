#!/bin/bash

# JobMailer Frontend Deployment Script

echo "🚀 Starting JobMailer Frontend Deployment..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Node.js and npm are installed"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Build the application
echo "🔨 Building the application..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi

echo "✅ Build completed successfully"

# Test the build
echo "🧪 Testing the build..."
npm start &
SERVER_PID=$!

# Wait for server to start
sleep 5

# Test if server is running
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Build test successful"
    kill $SERVER_PID
else
    echo "❌ Build test failed"
    kill $SERVER_PID
    exit 1
fi

echo "🎉 Frontend is ready for deployment!"
echo ""
echo "📋 Deployment Options:"
echo "1. Vercel (Recommended):"
echo "   - Install Vercel CLI: npm i -g vercel"
echo "   - Run: vercel --prod"
echo ""
echo "2. Manual deployment:"
echo "   - Upload the .next folder and package.json to your hosting platform"
echo "   - Run: npm start"
echo ""
echo "3. Static export (if needed):"
echo "   - Run: npm run export"
echo "   - Upload the 'out' folder to your static hosting"
echo ""
echo "🌐 API Base URL: https://jobmailer-dezw.onrender.com"
echo "📱 Frontend will be available at your deployment URL"
