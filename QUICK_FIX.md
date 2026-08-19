# 🔧 Quick Fix for Vercel Deployment

## Changes Made

1. **Created `/api/index.py`** - Standalone API file with all logic included
2. **Updated `vercel.json`** - Fixed routing configuration
3. **Updated `index.html`** - API calls now use `/api` prefix

## Deploy to Vercel

### Option 1: Push to GitHub (Recommended)

```bash
# Add new files
git add .

# Commit changes
git commit -m "Fix: Vercel deployment configuration"

# Push to GitHub
git push origin main
```

Vercel will automatically redeploy! ✅

### Option 2: Manual Deploy via CLI

```bash
# Install Vercel CLI if not installed
npm i -g vercel

# Deploy
vercel --prod
```

## Testing After Deployment

Visit your Vercel URL and test:

1. **API Health Check**: `https://your-app.vercel.app/api`
   - Should return: `{"message": "MOL-BHAAV API is running!"}`

2. **Prices Endpoint**: `https://your-app.vercel.app/api/prices`
   - Should return all mandi prices

3. **Main App**: `https://your-app.vercel.app`
   - Should load the UI
   - Try checking a price
   - View live prices section
   - Submit feedback

## If Still Not Working

### Check Vercel Logs

1. Go to Vercel Dashboard
2. Click on your project
3. Click "Deployments"
4. Click on latest deployment
5. Check "Function Logs" for errors

### Common Issues

**Issue**: 404 on API calls
**Fix**: Make sure routes in `vercel.json` are correct

**Issue**: Import errors
**Fix**: All code is now in single file `api/index.py`

**Issue**: CORS errors
**Fix**: `flask-cors` is installed in `requirements.txt`

## Environment Check

Make sure `requirements.txt` has:
```
Flask==3.1.2
flask-cors==6.0.2
Werkzeug==3.1.5
```

## Success Indicators

✅ Build completes without errors
✅ `/api` endpoint returns JSON
✅ `/api/prices` returns price data
✅ Frontend loads correctly
✅ Price check works
✅ Live prices display
✅ Feedback submission works

## Need Help?

Check Vercel logs for specific error messages and share them for debugging.
