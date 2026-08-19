# 🚀 Deployment Guide - MOL-BHAAV

## GitHub Setup

### Step 1: Initialize Git Repository

```bash
# Navigate to your project folder
cd mandi-app

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: MOL-BHAAV - AI Mandi Saathi"
```

### Step 2: Create GitHub Repository

1. Go to [github.com](https://github.com)
2. Click "New Repository"
3. Name: `mol-bhaav`
4. Description: "AI-Powered Mandi Price Comparison Tool for Indian Farmers"
5. Keep it Public
6. Don't initialize with README (we already have one)
7. Click "Create Repository"

### Step 3: Push to GitHub

```bash
# Add remote
git remote add origin https://github.com/daksh-builds/Molbhav.git

# Push code
git branch -M main
git push -u origin main
```

## Vercel Deployment

### Method 1: Via Vercel Dashboard (Recommended)

1. **Sign Up/Login to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Sign up with GitHub account

2. **Import Project**
   - Click "Add New..." → "Project"
   - Select your GitHub repository `mol-bhaav`
   - Click "Import"

3. **Configure Project**
   - Framework Preset: Other
   - Root Directory: `./`
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
   - Install Command: `pip install -r requirements.txt`

4. **Environment Variables** (Optional)
   - No environment variables needed for basic setup

5. **Deploy**
   - Click "Deploy"
   - Wait 1-2 minutes
   - Your app will be live! 🎉

### Method 2: Via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel

# Follow prompts:
# - Set up and deploy? Y
# - Which scope? (select your account)
# - Link to existing project? N
# - Project name? mol-bhaav
# - Directory? ./
# - Override settings? N

# Production deployment
vercel --prod
```

## Post-Deployment

### Your Live URLs

- **Production**: `https://mol-bhaav.vercel.app`
- **Preview**: `https://mol-bhaav-git-main-username.vercel.app`

### Update API URLs

The app automatically detects if it's running locally or on Vercel:
- Local: Uses `http://127.0.0.1:5000`
- Production: Uses relative URLs (same domain)

### Custom Domain (Optional)

1. Go to Vercel Dashboard → Your Project
2. Click "Settings" → "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions

## Testing Deployment

1. **Visit your live URL**
2. **Test features:**
   - ✅ Select item and check price
   - ✅ View live mandi prices
   - ✅ Submit feedback
   - ✅ Voice announcement works
   - ✅ Responsive on mobile

## Troubleshooting

### Issue: API calls failing
**Solution**: Check browser console for CORS errors. Ensure `flask-cors` is installed.

### Issue: Build fails
**Solution**: Verify `requirements.txt` has all dependencies:
```
Flask==3.1.2
flask-cors==6.0.2
Werkzeug==3.1.5
```

### Issue: 404 on routes
**Solution**: Check `vercel.json` routes configuration is correct.

### Issue: Slow cold starts
**Solution**: This is normal for free tier. Consider upgrading to Pro for faster response.

## Continuous Deployment

Once connected to GitHub, Vercel automatically:
- ✅ Deploys on every push to `main` branch
- ✅ Creates preview deployments for pull requests
- ✅ Runs builds and checks

## Monitoring

### View Logs
1. Go to Vercel Dashboard
2. Select your project
3. Click "Deployments"
4. Click on any deployment
5. View "Build Logs" and "Function Logs"

### Analytics
- Vercel provides free analytics
- View traffic, performance, and errors
- Go to Project → Analytics

## Updating Your App

```bash
# Make changes to your code
# Commit changes
git add .
git commit -m "Update: Added new feature"

# Push to GitHub
git push origin main

# Vercel automatically deploys! 🚀
```

## Cost

- **Vercel Free Tier**: Perfect for this project
  - Unlimited deployments
  - 100GB bandwidth/month
  - Serverless functions
  - Automatic HTTPS
  - Custom domains

## Support

If you face any issues:
1. Check [Vercel Documentation](https://vercel.com/docs)
2. Visit [Vercel Community](https://github.com/vercel/vercel/discussions)
3. Open an issue on your GitHub repo

---

**🎉 Congratulations! Your app is now live and accessible worldwide!**

Share your live URL:
- With hackathon judges
- On social media
- With farmers and users

**Live Demo**: `https://your-project.vercel.app`
