#!/bin/bash

# Advanced System Monitor - Quick Install Script
# Made by Satyam Jha

set -e

echo "🚀 Installing Advanced System Monitor..."
echo "Made by Satyam Jha"
echo "================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.6+ first."
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.6"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $python_version found. Python 3.6+ required."
    exit 1
fi

echo "✅ Python $python_version found"

# Install pip if not available
if ! command -v pip3 &> /dev/null; then
    echo "📦 Installing pip..."
    if [[ -n "$VIRTUAL_ENV" ]]; then
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python3 get-pip.py
        rm get-pip.py
    else
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python3 get-pip.py --user
        rm get-pip.py
    fi
fi

# Install psutil
echo "📦 Installing required dependencies..."
pip3 install psutil --user

# Download the system monitor
echo "📥 Downloading Advanced System Monitor..."
curl -sSL https://raw.githubusercontent.com/satyamjhablockdev/system_usage_tool/main/system_monitor.py -o system_monitor.py

# Make it executable
chmod +x system_monitor.py

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "📋 To run the monitor:"
echo "   python3 system_monitor.py"
echo ""
echo "📋 To run from anywhere, add to PATH:"
echo "   sudo cp system_monitor.py /usr/local/bin/system-monitor"
echo "   sudo chmod +x /usr/local/bin/system-monitor"
echo "   Then run: system-monitor"
echo ""
echo "🚀 Enjoy monitoring your system!"
echo "Made with ❤️  by Satyam Jha"
