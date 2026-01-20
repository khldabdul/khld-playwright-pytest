#!/bin/bash
# VPS Setup Script for E2E Test Reports
# Run this script on your VPS to set up the nginx configuration

set -e

# Configuration - Update these values
DOMAIN="${1:-reports.example.com}"
DEPLOY_PATH="${2:-/var/www/e2e-reports}"
SSL_EMAIL="${3:-admin@example.com}"

echo "========================================"
echo "E2E Reports VPS Setup"
echo "========================================"
echo "Domain: ${DOMAIN}"
echo "Deploy Path: ${DEPLOY_PATH}"
echo "========================================"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (sudo)"
    exit 1
fi

# Install nginx if not present
if ! command -v nginx &> /dev/null; then
    echo "Installing nginx..."
    apt-get update
    apt-get install -y nginx
fi

# Install certbot for SSL
if ! command -v certbot &> /dev/null; then
    echo "Installing certbot..."
    apt-get install -y certbot python3-certbot-nginx
fi

# Create deploy directory
echo "Creating directory structure..."
mkdir -p ${DEPLOY_PATH}
chown -R www-data:www-data ${DEPLOY_PATH}

# Create nginx configuration
echo "Creating nginx configuration..."
cat > /etc/nginx/sites-available/e2e-reports << EOF
server {
    listen 80;
    server_name ${DOMAIN};

    root ${DEPLOY_PATH};
    index index.html;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Serve static files
    location / {
        try_files \$uri \$uri/ =404;
        autoindex on;
        autoindex_exact_size off;
        autoindex_localtime on;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 1d;
        add_header Cache-Control "public, immutable";
    }

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
    gzip_min_length 1000;
}
EOF

# Enable site
ln -sf /etc/nginx/sites-available/e2e-reports /etc/nginx/sites-enabled/

# Test nginx configuration
echo "Testing nginx configuration..."
nginx -t

# Reload nginx
echo "Reloading nginx..."
systemctl reload nginx

# Setup SSL with Let's Encrypt
echo ""
echo "Setting up SSL certificate..."
certbot --nginx -d ${DOMAIN} --email ${SSL_EMAIL} --agree-tos --non-interactive --redirect

# Create initial index page
cat > ${DEPLOY_PATH}/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>E2E Test Reports</title>
    <style>
        body { font-family: system-ui; max-width: 800px; margin: 100px auto; text-align: center; }
        h1 { color: #4caf50; }
    </style>
</head>
<body>
    <h1>🧪 E2E Test Reports</h1>
    <p>Reports will appear here after the first test run.</p>
    <p>Push to main branch to trigger tests and deploy reports.</p>
</body>
</html>
EOF

# Set permissions
chown -R www-data:www-data ${DEPLOY_PATH}
chmod -R 755 ${DEPLOY_PATH}

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Your reports will be available at: https://${DOMAIN}/"
echo ""
echo "Next steps:"
echo "1. Add the following secrets to your GitHub repository:"
echo "   - VPS_SSH_KEY: Private SSH key for deployment"
echo "   - VPS_HOST: ${DOMAIN} (or IP address)"
echo "   - VPS_USER: Deploy user (see below)"
echo "   - VPS_DEPLOY_PATH: ${DEPLOY_PATH}"
echo ""
echo "2. Add the following variable to your GitHub repository:"
echo "   - REPORTS_DOMAIN: ${DOMAIN}"
echo ""
echo "3. Create a deploy user with SSH access:"
echo "   sudo useradd -m -s /bin/bash deploy"
echo "   sudo usermod -aG www-data deploy"
echo "   sudo mkdir -p /home/deploy/.ssh"
echo "   sudo chmod 700 /home/deploy/.ssh"
echo "   # Add your deploy public key to /home/deploy/.ssh/authorized_keys"
echo "   sudo chown -R deploy:deploy /home/deploy/.ssh"
echo "   sudo chown -R deploy:www-data ${DEPLOY_PATH}"
echo "   sudo chmod -R 775 ${DEPLOY_PATH}"
echo ""
