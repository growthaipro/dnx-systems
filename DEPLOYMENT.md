# Production Deployment Guide

## Prerequisites

- Python 3.11+
- PostgreSQL 13+
- Redis 6+
- Docker & Docker Compose (optional)
- SSL Certificate (for HTTPS)
- Domain name (for production)

## Deployment Checklist

### Environment Configuration
- [ ] Set `ENVIRONMENT=production`
- [ ] Set `DEBUG=False`
- [ ] Generate strong `SECRET_KEY` (minimum 32 characters)
- [ ] Configure PostgreSQL connection string
- [ ] Set up Redis for caching
- [ ] Configure CORS origins for frontend URL
- [ ] Set trusted hosts for your domain

### Security
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Set up API rate limiting
- [ ] Enable CORS appropriately
- [ ] Use environment variables for secrets
- [ ] Enable logging and monitoring
- [ ] Set up automated backups

### Database
- [ ] Create production database
- [ ] Run migrations: `alembic upgrade head`
- [ ] Enable database backups
- [ ] Configure connection pooling
- [ ] Set up monitoring

### API Deployment

#### Using Gunicorn (Recommended for Production)

```bash
# Install gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker main:app
```

#### Using Docker

```bash
# Build image
docker build -t dnx-systems-api .

# Run container
docker run -d \
  -e DATABASE_URL=postgresql://user:pass@host/db \
  -e SECRET_KEY=your-secret \
  -e ENVIRONMENT=production \
  -p 8000:8000 \
  dnx-systems-api
```

#### Using Docker Compose

```bash
# Update .env with production values
docker-compose -f docker-compose.prod.yml up -d
```

### Deployment Platforms

#### AWS EC2
```bash
# SSH to instance
ssh -i key.pem ubuntu@your-instance.amazonaws.com

# Clone and setup
git clone https://github.com/growthaipro/dnx-systems.git
cd dnx-systems/backend
pip install -r requirements.txt
cp .env.example .env

# Configure .env with production values
nano .env

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app &
```

#### AWS ECS/Fargate
- Push Docker image to ECR
- Create ECS task definition
- Create ECS service with load balancer
- Configure RDS for database
- Configure elasticache for Redis

#### Heroku
```bash
# Login to Heroku
heroku login

# Create app
heroku create dnx-systems-api

# Add PostgreSQL
heroku addons:create heroku-postgresql:standard-0

# Deploy
git push heroku main

# Run migrations
heroku run "python -c 'from core.database import init_db; init_db()'"
```

#### Google Cloud Run
```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/dnx-systems-api

# Deploy
gcloud run deploy dnx-systems-api \
  --image gcr.io/PROJECT_ID/dnx-systems-api \
  --platform managed \
  --region us-central1
```

#### DigitalOcean App Platform
- Connect GitHub repository
- Configure environment variables
- Select Python 3.11 runtime
- Add PostgreSQL database
- Deploy

### Nginx Configuration

Create `/etc/nginx/sites-available/dnx-systems`:

```nginx
upstream dnx_api {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name api.dnx-systems.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.dnx-systems.com;
    
    # SSL certificates
    ssl_certificate /etc/letsencrypt/live/api.dnx-systems.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.dnx-systems.com/privkey.pem;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Proxy settings
    location / {
        proxy_pass http://dnx_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/dnx-systems /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### SSL Certificate with Let's Encrypt

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d api.dnx-systems.com
```

### System Service (Systemd)

Create `/etc/systemd/system/dnx-systems.service`:

```ini
[Unit]
Description=DNX Systems API
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/home/www-data/dnx-systems/backend
Environment="PATH=/home/www-data/venv/bin"
ExecStart=/home/www-data/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 main:app

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable dnx-systems
sudo systemctl start dnx-systems
sudo systemctl status dnx-systems
```

### Monitoring

#### CloudWatch (AWS)
```python
# Add CloudWatch handler to logging
import watchtower
import logging

logger = logging.getLogger(__name__)
logger.addHandler(watchtower.CloudWatchLogHandler())
```

#### Sentry Error Tracking
```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="https://key@sentry.io/project-id",
    integrations=[FastApiIntegration()]
)
```

### Health Checks

Configure health check endpoints:
- `/health` - Basic health check
- `/api/v1` - API info endpoint

### Backups

```bash
# PostgreSQL backup
pg_dump -U user dnx_systems > backup.sql

# Automated backup with cron
0 2 * * * pg_dump -U user dnx_systems > /backups/$(date +\%Y\%m\%d).sql
```

### Logging

```bash
# View application logs
journalctl -u dnx-systems -f

# View Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Performance Optimization

1. **Enable Gzip Compression**
   ```nginx
   gzip on;
   gzip_types text/plain application/json;
   gzip_min_length 1000;
   ```

2. **Database Connection Pooling**
   - Already configured in SQLAlchemy

3. **Redis Caching**
   - Configured for session and data caching

4. **CDN** (for static content)
   - Use CloudFront, Cloudflare, or similar

### Scaling

1. **Horizontal Scaling**
   - Run multiple API instances
   - Use load balancer (AWS ELB, Nginx, etc.)
   - Shared PostgreSQL database
   - Shared Redis cache

2. **Database Scaling**
   - Use read replicas
   - Implement connection pooling
   - Archive old data

3. **Cache Strategy**
   - Cache frequently accessed data
   - Implement cache invalidation
   - Use Redis for distributed caching

## Production Environment Variables

```env
# Production
ENVIRONMENT=production
DEBUG=False

# Database
DATABASE_URL=postgresql://user:password@host:5432/dnx_systems

# Security
SECRET_KEY=your-64-character-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=https://app.dnx-systems.com,https://www.dnx-systems.com

# Hosts
ALLOWED_HOSTS=api.dnx-systems.com,*.dnx-systems.com

# Logging
LOG_LEVEL=INFO

# Email
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your-sendgrid-key

# Third-party APIs
STRIPE_SECRET_KEY=sk_live_xxxxx
STRIPE_PUBLIC_KEY=pk_live_xxxxx

# AWS
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_S3_BUCKET=dnx-systems-prod
AWS_REGION=us-east-1

# Redis
REDIS_URL=redis://user:password@host:6379/0

# Workers
WORKERS=4
```

## Troubleshooting

### API not responding
```bash
# Check if service is running
systemctl status dnx-systems

# Check port is listening
netstat -tlnp | grep 8000

# Check logs
journalctl -u dnx-systems -n 100
```

### Database connection issues
```bash
# Test connection
psql -h host -U user -d dnx_systems

# Check connection string
echo $DATABASE_URL
```

### High memory usage
- Increase swap space
- Optimize queries
- Reduce worker count
- Implement caching

## Support

For deployment issues, contact: support@growthaipro.com
