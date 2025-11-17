# 🎯 Qase Reporter Web UI - Complete Setup Guide

## ✅ Installation Complete!

Your Qase Reporter Web UI has been successfully created and configured!

## 📦 What's Been Created

### Core Application Files
- ✅ **app.py** - Main Streamlit web application (550+ lines)
- ✅ **qase_reporter.py** - Core reporter logic with API integration
- ✅ **config.py** - Configuration management
- ✅ **main.py** - CLI version (original)
- ✅ **list_tags.py** - Tag listing utility

### Documentation
- ✅ **README.md** - Comprehensive documentation
- ✅ **QUICK_START.md** - Quick start guide for beginners
- ✅ **SETUP_COMPLETE.md** - This file

### Launcher Scripts
- ✅ **run_app.bat** - Windows CMD launcher
- ✅ **run_app.ps1** - PowerShell launcher

### Dependencies
- ✅ **requirements.txt** - Updated with Streamlit
- ✅ **Virtual Environment** - Python 3.13 with all packages installed

## 🚀 How to Launch the Application

### Option 1: Using PowerShell Launcher (Recommended)
```powershell
cd d:\OTL\projects\Qase-Reporting\qase_reporting
.\run_app.ps1
```

### Option 2: Using CMD Launcher
```cmd
cd d:\OTL\projects\Qase-Reporting\qase_reporting
run_app.bat
```

### Option 3: Manual Launch
```powershell
cd d:\OTL\projects\Qase-Reporting\qase_reporting
.\venv\Scripts\Activate.ps1
streamlit run app.py
```

The application will open automatically in your default browser at:
**http://localhost:8501**

## 🎨 Application Features

### 1. Execute Tab 🚀
- **Run Report Button** - One-click execution
- **Real-time Progress** - Live progress bars and status updates
- **Execution Logs** - Detailed logging of all operations
- **Current Status** - Display of loaded data

### 2. Results Tab 📊
- **Summary Metrics**
  - 📦 Total Test Runs
  - 🧪 Total Tests Executed
  - ✅ Passed Tests (with pass rate %)
  - ❌ Failed Tests
  - 📊 Overall Pass Rate

- **Interactive Data Table**
  - Sortable columns
  - Search/filter functionality
  - Color-coded status indicators
  - Responsive layout

- **Export Options**
  - 📥 Download Excel - Instant download
  - 📥 Download CSV - Instant download
  - 💾 Save to Folder - Save to exports directory

### 3. Logs Tab 📋
- Real-time execution logs
- Color-coded messages (info/warning/error/success)
- Timestamp tracking
- Clear logs functionality

### 4. About Tab ℹ️
- Application information
- Feature list
- Usage instructions
- Documentation links
- Version information

### 5. Sidebar Configuration ⚙️
- **Project Settings**
  - Current project display
  - Export directory path

- **Fetch Options**
  - Max Test Runs slider (10-500)
  - Batch Size slider (10-100)

- **Tag Filtering** 🏷️
  - Enable/disable toggle
  - Include or Exclude mode
  - Comma-separated tag input
  - Live filter preview

- **Cache Management**
  - Clear cache button
  - Reset all loaded data

## 📋 Prerequisites Checklist

Before running the app, ensure you have:

- ✅ Python 3.8+ installed
- ✅ Virtual environment created and activated
- ✅ Dependencies installed (`pip install -r requirements.txt`)
- ✅ `.env` file created with credentials
- ✅ Valid Qase API token
- ✅ Correct project code

## 🔑 Setting Up .env File

Create a `.env` file in the `qase_reporting` directory:

```env
# Required - Get from Qase.io → Settings → API Tokens
QASE_API_TOKEN=your_qase_api_token_here

# Required - Your project code (e.g., ISP, DEMO, PROJ)
QASE_PROJECT_CODE=YOUR_PROJECT_CODE

# Optional - Directory for saving exports
EXPORT_DIR=exports

# Optional - API timeout in seconds
API_TIMEOUT=300

# Optional - Maximum results to fetch
MAX_RESULTS=1000
```

### How to Get Your API Token
1. Go to https://app.qase.io/
2. Click your profile icon (top right)
3. Select "Settings"
4. Navigate to "API Tokens"
5. Click "Generate New Token"
6. Copy the token
7. Paste it in your `.env` file

## 🎮 Usage Examples

### Example 1: Fetch All Test Runs
1. Launch the app
2. Go to Execute tab
3. Leave tag filtering disabled
4. Click "▶️ Run Report"
5. Wait for completion
6. View results in Results tab

### Example 2: Filter by Tags (Include)
1. Enable "Tag Filtering" in sidebar
2. Select "Include Tags"
3. Enter: `regression, smoke`
4. Click "▶️ Run Report"
5. Only runs with these tags will be fetched

### Example 3: Filter by Tags (Exclude)
1. Enable "Tag Filtering" in sidebar
2. Select "Exclude Tags"
3. Enter: `wip, draft`
4. Click "▶️ Run Report"
5. Runs with these tags will be excluded

### Example 4: Export Results
1. After running report, go to Results tab
2. Review the summary metrics
3. Use search to filter specific runs
4. Click "📥 Download Excel" for Excel file
5. Or click "💾 Save to Exports Folder" to keep local copy

## 🛠️ Installed Packages

Your virtual environment includes:

- **streamlit** (1.51.0) - Web UI framework
- **pandas** (2.3.3) - Data manipulation
- **requests** (2.31.0) - HTTP/API calls
- **openpyxl** (3.1.2) - Excel file handling
- **rich** (13.7.0) - Terminal formatting
- **python-dotenv** (1.0.0) - Environment variables
- **matplotlib** (3.8.2) - Plotting (for future features)
- **seaborn** (0.13.1) - Statistical visualizations
- **numpy** (1.26.3) - Numerical computing

## 📊 Project Structure

```
qase_reporting/
├── app.py                    # ⭐ Main Streamlit UI application
├── main.py                   # CLI version
├── qase_reporter.py          # Core reporter logic
├── config.py                 # Configuration management
├── list_tags.py              # Tag listing utility
├── requirements.txt          # Python dependencies
├── .env                      # ⚠️ Create this with your credentials
├── .gitignore               # Git ignore rules
├── README.md                # Full documentation
├── QUICK_START.md           # Quick start guide
├── SETUP_COMPLETE.md        # This file
├── run_app.bat              # Windows CMD launcher
├── run_app.ps1              # PowerShell launcher
├── exports/                 # Export directory
└── venv/                    # Virtual environment
```

## 🎯 Key Features Comparison

### Web UI (app.py) vs CLI (main.py)

| Feature | Web UI | CLI |
|---------|--------|-----|
| Interactive Interface | ✅ Yes | ❌ No |
| Real-time Progress | ✅ Yes | ⚠️ Limited |
| Summary Metrics | ✅ Yes | ❌ No |
| Search/Filter | ✅ Yes | ❌ No |
| Multiple Export Options | ✅ Yes | ⚠️ Limited |
| Execution Logs | ✅ Yes | ⚠️ Console only |
| Tag Filtering UI | ✅ Yes | ⚠️ Interactive prompt |
| No Code Required | ✅ Yes | ❌ Command line |

**Recommendation:** Use Web UI for daily usage, CLI for automation/scripting

## 🔧 Advanced Configuration

### Performance Tuning

For large projects (1000+ test runs):
- Set Max Test Runs: 100-200
- Set Batch Size: 30-50
- Enable tag filtering to narrow results

For small projects (<100 test runs):
- Set Max Test Runs: 500
- Set Batch Size: 50-100
- Fetch all runs for complete analysis

### Custom Export Directory

Edit `.env`:
```env
EXPORT_DIR=D:\MyReports\Qase
```

The app will create the directory if it doesn't exist.

## 🐛 Troubleshooting

### App Won't Start
```powershell
# Check if Streamlit is installed
pip list | Select-String streamlit

# Reinstall if needed
pip install --upgrade streamlit

# Verify Python version
python --version  # Should be 3.8+
```

### Import Errors
```powershell
# Activate virtual environment first
.\venv\Scripts\Activate.ps1

# Reinstall all dependencies
pip install -r requirements.txt
```

### Browser Doesn't Open
- Manually open: http://localhost:8501
- Check if port 8501 is available
- Check firewall settings

### Configuration Errors
- Verify `.env` file exists
- Check for typos in `.env`
- Ensure no extra spaces around values
- Restart the app after changing `.env`

## 📈 Future Enhancements (Planned)

- 📊 Interactive charts and graphs
- 📅 Date range filtering
- 👥 Team member filtering
- 📧 Email report scheduling
- 🔔 Webhook notifications
- 💾 Report history and caching
- 📱 Mobile-responsive design
- 🌙 Dark mode toggle

## 💡 Tips for Best Experience

1. **Start Small**: Fetch 10-20 runs first to test
2. **Use Tags**: Organize your test runs with tags
3. **Regular Exports**: Save important reports
4. **Monitor Logs**: Check for warnings/errors
5. **Clear Cache**: Refresh data when needed
6. **Bookmark**: Add http://localhost:8501 to favorites

## 📞 Support & Resources

- **Full Documentation**: See README.md
- **Quick Start**: See QUICK_START.md
- **Qase API Docs**: https://developers.qase.io/
- **Streamlit Docs**: https://docs.streamlit.io/
- **Qase Status**: https://status.qase.io/

## ✅ Final Checklist

Before your first run:

- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] `.env` file created
- [ ] API token added to `.env`
- [ ] Project code added to `.env`
- [ ] Test run executed successfully
- [ ] Results viewed in browser
- [ ] Export tested

## 🎉 You're All Set!

Your Qase Reporter Web UI is ready to use!

### Quick Start Command:
```powershell
cd d:\OTL\projects\Qase-Reporting\qase_reporting
.\run_app.ps1
```

**Enjoy your new testing dashboard! 🚀**

---

*Setup completed on: November 17, 2025*
*Version: 1.0.0*
