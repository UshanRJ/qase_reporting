# 📊 Qase Test Run Reporter - Web UI

A modern, interactive web interface for analyzing Qase test run results with real-time data fetching, visualization, and export capabilities.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

- 🚀 **Interactive Web UI** - Modern, user-friendly interface built with Streamlit
- 📊 **Real-time Data Fetching** - Fetch test runs and results directly from Qase API
- 🏷️ **Tag Filtering** - Include or exclude test runs by tags
- 📈 **Summary Metrics** - Visual dashboard with key performance indicators
- 🔍 **Search & Filter** - Quickly find specific test runs
- 📥 **Multiple Export Formats** - Export to Excel, CSV, or save to local folder
- 📋 **Execution Logs** - Track all operations with detailed logging
- ⚡ **Batch Processing** - Configurable batch sizes for optimal performance

## 📋 Prerequisites

- Python 3.8 or higher
- Qase API Token
- Qase Project Code

## 🚀 Quick Start

### 1. Clone or Download the Project

```bash
cd d:\OTL\projects\Qase-Reporting\qase_reporting
```

### 2. Create Virtual Environment (Recommended)

```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

```cmd
# Windows CMD
python -m venv venv
venv\Scripts\activate.bat
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the `qase_reporting` directory:

```env
# Required
QASE_API_TOKEN=your_qase_api_token_here
QASE_PROJECT_CODE=YOUR_PROJECT_CODE

# Optional
EXPORT_DIR=exports
API_TIMEOUT=300
MAX_RESULTS=1000
```

**How to get your Qase API Token:**
1. Log in to [Qase.io](https://app.qase.io/)
2. Go to Settings → API Tokens
3. Click "Generate New Token"
4. Copy the token and paste it in `.env`

### 5. Run the Web Application

```bash
streamlit run app.py
```

The application will automatically open in your default browser at `http://localhost:8501`

## 📖 Usage Guide

### Main Interface

1. **Execute Tab** 🚀
   - Click "Run Report" to fetch test data
   - Monitor progress in real-time
   - View current status and loaded data

2. **Results Tab** 📊
   - View summary metrics (Total Runs, Tests, Pass Rate, etc.)
   - Browse detailed results table
   - Search/filter test runs
   - Export data (Excel, CSV, or save to folder)

3. **Logs Tab** 📋
   - Monitor execution logs
   - Track errors and warnings
   - Clear logs as needed

4. **About Tab** ℹ️
   - View application information
   - Access documentation links
   - Check version info

### Sidebar Configuration

- **Project Settings**: View current project and export directory
- **Fetch Options**: 
  - Max Test Runs: Limit number of runs to fetch (10-500)
  - Batch Size: Number of results per batch (10-100)
- **Tag Filtering**:
  - Enable/disable tag filtering
  - Choose Include or Exclude mode
  - Enter comma-separated tags
- **Clear Cache**: Reset all loaded data

### Tag Filtering Examples

**Include specific tags:**
```
regression, smoke
```
Only fetches test runs tagged with "regression" OR "smoke"

**Exclude specific tags:**
```
wip, draft
```
Fetches all test runs EXCEPT those tagged with "wip" OR "draft"

## 📁 Project Structure

```
qase_reporting/
├── app.py                    # Streamlit web application
├── main.py                   # CLI version (original)
├── qase_reporter.py          # Core reporter logic
├── config.py                 # Configuration management
├── list_tags.py              # Tag listing utility
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create this)
├── .gitignore               # Git ignore rules
├── exports/                  # Default export directory
└── README.md                # This file
```

## 🛠️ Troubleshooting

### Application won't start

**Error: `streamlit: command not found`**
```bash
pip install --upgrade streamlit
```

**Error: `Import "streamlit" could not be resolved`**
- Ensure you've activated your virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

### Configuration Issues

**Error: `QASE_API_TOKEN not found`**
- Create `.env` file in the correct directory
- Ensure the token is valid (no extra spaces)
- Restart the application after creating `.env`

**Error: `Project code not configured`**
- Add `QASE_PROJECT_CODE=YOUR_CODE` to `.env`
- Replace `YOUR_CODE` with your actual project code

### API/Network Issues

**Error: `Failed to fetch test runs`**
- Check your internet connection
- Verify API token is still valid
- Check Qase API status: https://status.qase.io/
- Try increasing `API_TIMEOUT` in `.env`

**Error: `No test runs found`**
- Verify test runs exist in your project
- Check tag filters (they might be too restrictive)
- Try fetching without tag filtering first

### Export Issues

**Error: `Error exporting to Excel`**
- Ensure `openpyxl` is installed: `pip install openpyxl`
- Check write permissions in the export directory
- Verify export directory exists

## 📦 Dependencies

- **streamlit** - Web application framework
- **pandas** - Data manipulation and analysis
- **requests** - HTTP library for API calls
- **openpyxl** - Excel file handling
- **rich** - Terminal formatting (for CLI version)
- **python-dotenv** - Environment variable management

## 🔧 Advanced Configuration

### Custom Export Directory

Add to `.env`:
```env
EXPORT_DIR=D:\MyReports\Qase
```

### API Rate Limiting

Add to `.env`:
```env
API_TIMEOUT=300
MAX_RESULTS=2000
```

### Performance Tuning

For large projects, adjust batch size:
- Smaller batch (10-20): Slower but more stable
- Larger batch (50-100): Faster but may timeout

## 📊 CLI Version

For command-line usage, run the original script:

```bash
python main.py
```

The CLI version offers:
- Interactive tag selection
- Direct console output
- Automated export to files

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests.

## 📄 License

MIT License - feel free to use this project for your testing needs.

## 🔗 Resources

- [Qase API Documentation](https://developers.qase.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/)

## 💡 Tips

1. **First Time Use**: Start with no tag filtering to see all available data
2. **Performance**: Use smaller batch sizes if you experience timeouts
3. **Tags**: Tag names are case-insensitive
4. **Exports**: Use "Save to Exports Folder" for local archiving
5. **Logs**: Monitor the Logs tab for troubleshooting

## 📞 Support

For issues or questions:
1. Check the Logs tab for error details
2. Review the Troubleshooting section above
3. Verify your `.env` configuration
4. Check Qase API status

---

**Built with ❤️ using Streamlit and Qase API**

Last Updated: November 17, 2025
