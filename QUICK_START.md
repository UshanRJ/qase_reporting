# 🚀 Quick Start Guide - Qase Reporter Web UI

Get started in 5 minutes!

## ⚡ Super Quick Start (For Experienced Users)

```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file with your credentials
# QASE_API_TOKEN=your_token
# QASE_PROJECT_CODE=your_code

# 3. Run the app
streamlit run app.py
```

## 📋 Detailed Step-by-Step Guide

### Step 1: Install Python (if not already installed)
- Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
- During installation, check "Add Python to PATH"

### Step 2: Open Terminal in Project Directory
```powershell
cd d:\OTL\projects\Qase-Reporting\qase_reporting
```

### Step 3: Create Virtual Environment (Recommended)
```powershell
# PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# CMD
python -m venv venv
venv\Scripts\activate.bat
```

### Step 4: Install Dependencies
```powershell
pip install -r requirements.txt
```

This will install:
- ✅ Streamlit (Web UI framework)
- ✅ Pandas (Data processing)
- ✅ Requests (API calls)
- ✅ OpenPyXL (Excel export)
- ✅ Rich (Terminal formatting)
- ✅ Other dependencies

### Step 5: Configure API Credentials

Create a file named `.env` in the `qase_reporting` folder:

```env
QASE_API_TOKEN=your_qase_api_token_here
QASE_PROJECT_CODE=YOUR_PROJECT_CODE
EXPORT_DIR=exports
```

**How to get your API Token:**
1. Go to https://app.qase.io/
2. Click your profile → Settings
3. Navigate to "API Tokens"
4. Click "Generate New Token"
5. Copy the token and paste it in `.env`

### Step 6: Launch the Application

**Option A: Using Launcher Scripts (Easiest)**
```powershell
# PowerShell
.\run_app.ps1

# CMD
run_app.bat
```

**Option B: Manual Launch**
```powershell
streamlit run app.py
```

### Step 7: Use the Application

1. **Browser Opens Automatically** at `http://localhost:8501`
   
2. **Configure in Sidebar:**
   - Set max test runs to fetch
   - Set batch size
   - Enable tag filtering (optional)

3. **Execute Tab:**
   - Click "▶️ Run Report" button
   - Wait for data to load
   - Monitor progress

4. **Results Tab:**
   - View summary metrics
   - Browse detailed results
   - Search/filter data
   - Export to Excel or CSV

5. **Export Data:**
   - Click "📥 Download Excel" for Excel file
   - Click "📥 Download CSV" for CSV file
   - Click "💾 Save to Exports Folder" to save locally

## 🎯 Common Use Cases

### Use Case 1: Fetch All Test Runs
1. Go to Execute tab
2. Leave tag filtering disabled
3. Click "Run Report"
4. View results in Results tab

### Use Case 2: Filter by Tags
1. Enable "Tag Filtering" in sidebar
2. Select "Include Tags" or "Exclude Tags"
3. Enter tags (e.g., `regression, smoke`)
4. Click "Run Report"

### Use Case 3: Export Results
1. After running report, go to Results tab
2. Choose export format:
   - Excel: Best for analysis in Excel/Google Sheets
   - CSV: Best for importing to other tools
   - Save to Folder: Keep local archive

## 🔧 Troubleshooting

### "streamlit: command not found"
```powershell
# Make sure you activated the virtual environment
.\venv\Scripts\Activate.ps1

# Reinstall streamlit
pip install streamlit
```

### "Configuration Error: QASE_API_TOKEN not found"
- Check that `.env` file exists in the correct folder
- Verify no extra spaces in the file
- Make sure the file is named `.env` (not `.env.txt`)

### "No test runs found"
- Verify your project code is correct
- Check if test runs exist in Qase
- Try without tag filtering first
- Verify API token has correct permissions

### Application is slow
- Reduce "Max Test Runs" in sidebar
- Reduce "Batch Size" in sidebar
- Check your internet connection

## 💡 Tips & Tricks

1. **First Time:** Start with 10-20 test runs to test the setup
2. **Tags:** Tag names are case-insensitive
3. **Search:** Use the search box in Results tab to filter data
4. **Cache:** Click "Clear Cache" in sidebar to refresh data
5. **Logs:** Check Logs tab if something goes wrong

## 🎓 Video Tutorial (Coming Soon)

Watch our video tutorial at: [Link to be added]

## 📞 Need Help?

1. Check the **Logs tab** for error messages
2. Review the **About tab** for documentation links
3. Read the full **README.md** for advanced topics
4. Check **Qase API Status**: https://status.qase.io/

## ✅ Next Steps

Once you're comfortable with the basics:
- Experiment with tag filtering
- Try different batch sizes for performance
- Export data to analyze trends
- Schedule automated reports (advanced)

---

**Happy Testing! 🧪**

*Last Updated: November 17, 2025*
