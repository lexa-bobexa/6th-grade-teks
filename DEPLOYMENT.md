# Deployment Guide

Complete guide for deploying TEKS Grade 6 Math Tutor to production.

## 📋 Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment Options](#cloud-deployment-options)
4. [Environment Configuration](#environment-configuration)
5. [Production Checklist](#production-checklist)

---

## 🔧 Local Development

### Backend

```bash
# 1. Install dependencies
pip install -e .

# 2. Run development server
uvicorn api.main:app --reload --port 8000

# Server: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Frontend

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Run development server
npm run dev

# App: http://localhost:5173
```

---

## 🐳 Docker Deployment

### Single Container

```bash
# Build image
docker build -t teks-grade6 .

# Run container
docker run -d \
  -p 8000:8000 \
  --name teks-tutor \
  teks-grade6

# View logs
docker logs -f teks-tutor
```

### Docker Compose (Full Stack)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENV=production
      - CORS_ORIGINS=https://yourdomain.com
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - backend
    restart: unless-stopped
```

Frontend Dockerfile (`frontend/Dockerfile`):

```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Frontend nginx config (`frontend/nginx.conf`):

```nginx
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Run with Docker Compose:

```bash
docker-compose up -d
```

---

## ☁️ Cloud Deployment Options

### Option 1: Render.com (Easiest)

**Backend:**
1. Create new Web Service
2. Connect GitHub repo
3. Build command: `pip install -e .`
4. Start command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
5. Set environment variables

**Frontend:**
1. Create new Static Site
2. Build command: `cd frontend && npm install && npm run build`
3. Publish directory: `frontend/dist`

### Option 2: Railway.app

1. Connect GitHub repository
2. Railway auto-detects Python/Node.js
3. Configure environment variables
4. Deploy with one click

### Option 3: Vercel (Frontend) + Railway (Backend)

**Frontend (Vercel):**
```bash
cd frontend
npm install -g vercel
vercel
```

**Backend (Railway):**
1. Create new project from GitHub
2. Set start command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

### Option 4: AWS (Advanced)

**Backend (ECS + Fargate):**
```bash
# Build and push to ECR
aws ecr create-repository --repository-name teks-tutor
docker tag teks-grade6:latest <account>.dkr.ecr.us-east-1.amazonaws.com/teks-tutor
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/teks-tutor

# Deploy to ECS
aws ecs create-cluster --cluster-name teks-cluster
aws ecs create-service --cluster teks-cluster --service-name teks-service
```

**Frontend (S3 + CloudFront):**
```bash
cd frontend
npm run build
aws s3 sync dist/ s3://teks-tutor-frontend
aws cloudfront create-invalidation --distribution-id <id> --paths "/*"
```

### Option 5: DigitalOcean App Platform

1. Connect GitHub repo
2. Configure components:
   - **Backend**: Python app, port 8000
   - **Frontend**: Static site from `frontend/dist`
3. Set environment variables
4. Deploy

---

## 🔐 Environment Configuration

### Backend (.env)

```bash
# API Configuration
ENV=production
HOST=0.0.0.0
PORT=8000
WORKERS=4

# CORS
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Optional: OpenAI for enhanced problem generation
OPENAI_API_KEY=sk-...

# Optional: Database (if adding persistence)
DATABASE_URL=postgresql://user:pass@host:5432/teks_tutor
```

### Frontend (.env)

```bash
# API endpoint
VITE_API_URL=https://api.yourdomain.com
```

---

## ✅ Production Checklist

### Backend

- [ ] Set `ENV=production` in environment
- [ ] Configure CORS origins properly
- [ ] Enable HTTPS/SSL certificates
- [ ] Set up health check endpoint monitoring
- [ ] Configure logging (JSON format for cloud)
- [ ] Enable API rate limiting (if needed)
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Test all API endpoints in production
- [ ] Set up automated backups (if using DB)

### Frontend

- [ ] Update API base URL to production
- [ ] Build with `npm run build`
- [ ] Test all routes in production
- [ ] Verify CORS configuration
- [ ] Enable HTTPS/SSL
- [ ] Configure CDN (CloudFlare, etc.)
- [ ] Set up analytics (Google Analytics, Plausible)
- [ ] Test offline functionality
- [ ] Verify MathJax loads correctly
- [ ] Test on mobile devices

### Security

- [ ] Use HTTPS everywhere
- [ ] Set secure headers (HSTS, CSP, etc.)
- [ ] Validate all user inputs
- [ ] Rate limit API endpoints
- [ ] Keep dependencies updated
- [ ] Regular security audits
- [ ] COPPA/FERPA compliance (student data)

### Performance

- [ ] Enable gzip/brotli compression
- [ ] Configure CDN for static assets
- [ ] Optimize images and SVGs
- [ ] Enable browser caching
- [ ] Monitor response times
- [ ] Set up uptime monitoring

### Monitoring

- [ ] Health check endpoint `/health`
- [ ] Application logs
- [ ] Error tracking
- [ ] Performance metrics
- [ ] User analytics
- [ ] Cost monitoring (cloud)

---

## 🔄 CI/CD Pipeline

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -e .
      - name: Run tests
        run: pytest tests/

  deploy-backend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Render
        run: curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}

  deploy-frontend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Vercel
        run: |
          cd frontend
          npm install -g vercel
          vercel --prod --token=${{ secrets.VERCEL_TOKEN }}
```

---

## 📊 Monitoring & Logging

### Health Check

The `/health` endpoint returns:

```json
{
  "status": "ok",
  "timestamp": "2025-09-29T19:00:00Z",
  "version": "1.0.0"
}
```

Monitor this endpoint with:
- UptimeRobot
- Pingdom
- StatusCake
- CloudWatch (AWS)

### Application Logs

Backend logs include:
- Request/response times
- Error stack traces
- Item generation metrics
- Grading results

Frontend logs include:
- User interactions
- API errors
- Performance metrics
- Mastery updates

---

## 🆘 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.11+

# Verify dependencies
pip list

# Check port availability
lsof -i :8000
```

### Frontend build fails
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install

# Check Node version
node --version  # Should be 18+
```

### CORS errors
- Verify `CORS_ORIGINS` in backend env
- Check frontend API URL configuration
- Ensure HTTPS is used in production

### MathJax not rendering
- Check browser console for errors
- Verify MathJax CDN is accessible
- Test with simple LaTeX: `$x + 1$`

---

## 📞 Support

For deployment issues:
1. Check logs first
2. Review this guide
3. Open GitHub issue with:
   - Deployment platform
   - Error messages
   - Steps to reproduce

---

**Happy Deploying! 🚀**
