# 🚂 Railway Deployment Guide for FastMCP iOS Automation Server

This guide will help you deploy your FastMCP iOS automation server to Railway.

## 📋 Prerequisites

1. Railway account (sign up at https://railway.app)
2. Railway CLI installed (optional but recommended)
3. GitHub repository with your code

## 🚀 Deployment Steps

### Option 1: Deploy via GitHub (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Add Railway deployment configuration"
   git push origin main
   ```

2. **Connect to Railway**
   - Go to https://railway.app/new
   - Click "Deploy from GitHub repo"
   - Authorize Railway to access your GitHub
   - Select your repository

3. **Configure Environment Variables**
   In Railway dashboard, add these variables:
   ```
   MCP_TRANSPORT=sse
   RAILWAY_ENVIRONMENT=production
   ```

4. **Deploy**
   - Railway will automatically detect the Dockerfile
   - The deployment will start automatically
   - Monitor the build logs

### Option 2: Deploy via Railway CLI

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize project**
   ```bash
   railway init
   ```

4. **Deploy**
   ```bash
   railway up
   ```

## 🔧 Configuration

### Environment Variables

Railway automatically provides:
- `PORT` - The port your app should listen on
- `RAILWAY_ENVIRONMENT` - The deployment environment

Your app uses these additional variables:
- `MCP_TRANSPORT` - Set to "sse" for cloud deployment
- `MCP_HOST` - Automatically set to "0.0.0.0" in cloud mode

### Health Checks

The server provides a health endpoint at `/health` that Railway uses to monitor your app's status.

## 🧪 Testing Your Deployment

1. **Check deployment status**
   ```bash
   curl https://your-app.railway.app/health
   ```

2. **Test SSE endpoint**
   ```bash
   curl https://your-app.railway.app/sse
   ```

3. **View logs**
   - In Railway dashboard, click on your service
   - Go to "Logs" tab

## ⚠️ Important Notes

### iOS Automation Limitations in Cloud

Since iOS simulators cannot run in cloud environments, the automation tools will return error messages when called. The server will still run and be accessible for:
- Health monitoring
- API testing
- Integration with other services

To use the actual iOS automation features, you need to run the server locally with access to macOS and Xcode.

### Claude Desktop Integration

Claude Desktop requires MCP servers to use stdio transport and run locally. To connect Claude Desktop to your Railway deployment, you would need to create a local proxy server. However, the iOS automation features still require local simulator access.

## 🔍 Troubleshooting

### 502 Bad Gateway Error

If you see a 502 error:
1. Check the deployment logs for errors
2. Ensure the PORT environment variable is being used
3. Verify the server is binding to 0.0.0.0, not 127.0.0.1

### Build Failures

Common issues:
1. **Missing dependencies**: Check requirements.txt
2. **Dockerfile issues**: Ensure paths are correct
3. **Python version**: Railway uses the version specified in Dockerfile

### Server Not Starting

Check:
1. Port configuration is using `os.getenv("PORT")`
2. Host is set to "0.0.0.0" for cloud
3. No syntax errors in Python code

## 📊 Monitoring

Railway provides:
- Real-time logs
- Resource usage metrics
- Deployment history
- Custom domains

Access these in your Railway dashboard under your project.

## 🔗 Useful Links

- [Railway Documentation](https://docs.railway.app)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [MCP Protocol Specification](https://modelcontextprotocol.io)

## 💡 Next Steps

1. Set up custom domain in Railway settings
2. Configure alerts for downtime
3. Set up GitHub Actions for CI/CD
4. Consider implementing a local proxy for Claude Desktop integration 