#!/bin/bash
# Installation script for Ubuntu/Debian

echo "================================================"
echo "Telegram Auto Order Bot - Installation Script"
echo "================================================"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo "❌ Please do not run as root"
    exit 1
fi

# Update system
echo "📦 Updating system packages..."
sudo apt update

# Install Python and pip
echo "🐍 Installing Python and pip..."
sudo apt install -y python3 python3-pip python3-venv

# Install MongoDB
echo "🍃 Installing MongoDB..."
if ! command -v mongod &> /dev/null; then
    sudo apt install -y mongodb
    sudo systemctl start mongodb
    sudo systemctl enable mongodb
    echo "✅ MongoDB installed and started"
else
    echo "✅ MongoDB already installed"
fi

# Install Git
echo "📚 Installing Git..."
sudo apt install -y git

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Setup configuration
if [ ! -f .env ]; then
    echo "⚙️  Setting up configuration..."
    cp .env.example .env
    echo ""
    echo "================================================"
    echo "⚠️  IMPORTANT: Please edit .env file with your credentials"
    echo "================================================"
    echo ""
    echo "You need to set:"
    echo "  - API_ID (from my.telegram.org)"
    echo "  - API_HASH (from my.telegram.org)"
    echo "  - BOT_TOKEN (from @BotFather)"
    echo "  - ADMIN_IDS (your Telegram user ID)"
    echo ""
    echo "Edit with: nano .env"
    echo ""
else
    echo "✅ Configuration file already exists"
fi

# Create logs directory
mkdir -p logs

echo ""
echo "================================================"
echo "✅ Installation complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file: nano .env"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Setup sample data (optional): python setup_sample_data.py"
echo "4. Run bot: python main.py"
echo ""
echo "For systemd service setup, see DEPLOYMENT.md"
echo ""
