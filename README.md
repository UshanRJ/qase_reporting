# 📊 Qase Test Run Reporter - Web UI

A modern, interactive web interface for analyzing Qase test run results with real-time data fetching, visualization, and export capabilities.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

### Core Features
- 🚀 **Interactive Web UI** - Modern, user-friendly interface built with Streamlit
- 📊 **Real-time Data Fetching** - Fetch test runs and results directly from Qase API
- 🏷️ **Advanced Tag Filtering** - Include or exclude test runs by tags with flexible matching
- 🎯 **Milestone Filtering** - Filter test runs by sprint/release milestones with multi-select
- 📈 **Summary Metrics** - Visual dashboard with key performance indicators
- 🔍 **Search & Filter** - Quickly find specific test runs in results table
- 📥 **Multiple Export Formats** - Export to Excel, CSV, or save to local folder
- 📋 **Execution Logs** - Track all operations with detailed logging
- ⚡ **Batch Processing** - Configurable batch sizes for optimal performance

### Security Features
- 🔐 **User Authentication** - Multi-user login system for controlled access
- 🔒 **Session Management** - Secure session-based authentication
- 👥 **Multi-User Support** - Different credentials for different users
- 🚪 **Logout Functionality** - Users can securely logout anytime

### Advanced Features
- 🔄 **Combined Filtering** - Use tag and milestone filters together
- 📊 **Smart Caching** - Milestones cached per session to reduce API calls
- 💾 **Session State** - Preserve data between reruns
- 📈 **Progress Tracking** - Real-time progress bars for long operations
- 🎨 **Responsive Design** - Works on desktop and tablet devices

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

### 5. Configure Authentication (for Streamlit Cloud Deployment)

For local development with authentication, create `.streamlit/secrets.toml`:

```toml
# Qase API Configuration
QASE_API_TOKEN = "your_qase_api_token_here"
QASE_PROJECT_CODE = "ISP"

# Multi-User Authentication
[users]
admin = "admin"
# Add more users as needed
```

> 📖 **Note**: `.streamlit/secrets.toml` is gitignored. For Streamlit Cloud deployment, add secrets in the dashboard.

### 6. Run the Web Application

```bash
streamlit run app.py
```

**Alternative**: Use the provided launcher scripts:

```powershell
# Windows PowerShell
.\run_app.ps1
```

```cmd
# Windows CMD
run_app.bat
```

The application will automatically open in your default browser at `http://localhost:8501`

### 7. Login (if authentication is enabled)

If authentication is enabled, you'll see a login page:
- **Username**: `admin`
- **Password**: `admin`

> 🔐 These are the default credentials. Change them in `.streamlit/secrets.toml` for production use.

## 📖 Usage Guide

### Authentication

When the app starts, you'll see a login page:
1. Enter your **Username** (e.g., `admin`)
2. Enter your **Password** (e.g., `admin`)
3. Click **Login**
4. You'll see the main dashboard
5. Use **Logout** button in sidebar to logout


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
- **Milestone Filtering**:
  - Enable/disable milestone filtering
  - Multi-select from available milestones
  - Works alongside tag filtering
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

### Milestone Filtering Examples

**Filter by single milestone:**
- Select "IBNU Sprint 60 - IS Feature" from dropdown
- Retrieves only test runs associated with that milestone

**Filter by multiple milestones:**
- Select "IBNU Sprint 60 - IS Feature" AND "IBNU Sprint 60 - IS+ PowerBI"
- Retrieves test runs from any of the selected milestones

**Combined filtering:**
- Enable both Tag Filtering (Include: "regression") and Milestone Filtering (Sprint 60)
- Retrieves only regression test runs from Sprint 60

## 📁 Project Structure

```
qase_reporting/
├── app.py                           # Streamlit web application (main entry)
├── auth.py                          # Authentication module
├── qase_reporter.py                 # Core reporter with tag/milestone filtering
├── config.py                        # Configuration management
├── main.py                          # CLI version (legacy)
├── list_tags.py                     # Tag listing utility
├── test_milestones.py               # Milestone filtering test script
├── requirements.txt                 # Python dependencies
├── .env                             # Local environment variables (create this)
├── .gitignore                       # Git ignore rules
├── .streamlit/
│   ├── config.toml                  # Streamlit app configuration
│   ├── secrets.toml                 # Local secrets (create this, gitignored)
│   └── secrets.toml.template        # Template for secrets
├── exports/                         # Default export directory
├── README.md                        # This file
├── AUTHENTICATION_GUIDE.md          # Authentication setup guide
├── DEPLOYMENT_CHECKLIST.md          # Deployment quick reference
├── MILESTONE_FILTERING.md           # Milestone feature documentation
├── run_app.bat                      # Windows CMD launcher
└── run_app.ps1                      # PowerShell launcher
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
- Ensure the token is valid (no extra spaces or quotes)
- Restart the application after creating `.env`
- For Streamlit, also check `.streamlit/secrets.toml`

**Error: `Project code not configured`**
- Add `QASE_PROJECT_CODE=YOUR_CODE` to `.env`
- Replace `YOUR_CODE` with your actual project code

### Authentication Issues

**Can't login / Invalid credentials**
- Check `.streamlit/secrets.toml` has the correct `[users]` section
- Verify username and password match exactly (case-sensitive)
- Clear browser cache and try again
- Check that secrets.toml is in `.streamlit/` directory

**Login page not showing**
- Authentication may be disabled
- Check `app.py` has `check_multi_user_password()` call
- Verify `auth.py` is in the same directory

### API/Network Issues

**Error: `Failed to fetch test runs`**
- Check your internet connection
- Verify API token is still valid
- Check Qase API status: https://status.qase.io/
- Try increasing `API_TIMEOUT` in `.env`

**Error: `No test runs found`**
- Verify test runs exist in your project
- Check tag filters (they might be too restrictive)
- Check milestone filters (may exclude all runs)
- Try fetching without any filtering first
- Verify you have access to the project in Qase

### Export Issues

**Error: `Error exporting to Excel`**
- Ensure `openpyxl` is installed: `pip install openpyxl`
- Check write permissions in the export directory
- Verify export directory exists

## 📦 Dependencies

Core Libraries:
- **streamlit** - Web application framework
- **pandas** - Data manipulation and analysis
- **requests** - HTTP library for API calls
- **openpyxl** - Excel file handling
- **rich** - Terminal formatting (for CLI version)
- **python-dotenv** - Environment variable management

All dependencies are listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

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

### Authentication Configuration

#### Add Multiple Users
Edit `.streamlit/secrets.toml`:
```toml
[users]
admin = "admin_secure_password"
qa_team = "team_password"
developer = "dev_password"
```

#### Change Passwords
Update the password value for any user:
```toml
[users]
admin = "new_secure_password_here"
```

#### Disable Authentication (Local Development Only)
Comment out the authentication check in `app.py`:
```python
# if not check_multi_user_password():
#     st.stop()
#     return
```

> ⚠️ **Warning**: Never deploy without authentication in production!

## 🌐 Deployment to Streamlit Cloud

### Quick Deploy
1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Click "New app" and select your repository
4. Set main file: `qase_reporting/app.py`
5. Add secrets in the dashboard (see below)
6. Deploy!

### Configure Secrets
In Streamlit Cloud dashboard → App Settings → Secrets, add:

```toml
QASE_API_TOKEN = "your_actual_token_here"
QASE_PROJECT_CODE = "ISP"

[users]
admin = "admin"
# Add more users as needed
```

### Important Notes
- ✅ App URL is public but **login is required**
- ✅ Only users with credentials can access
- ✅ All secrets are encrypted in Streamlit Cloud
- ✅ Never commit `.streamlit/secrets.toml` to GitHub


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

### External Resources
- [Qase API Documentation](https://developers.qase.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Cloud Deployment](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
- [Pandas Documentation](https://pandas.pydata.org/)

## 💡 Tips & Best Practices

### General Usage
1. **First Time Use**: Start with no filtering to see all available data
2. **Performance**: Use smaller batch sizes if you experience timeouts
3. **Tags**: Tag names are case-insensitive for matching
4. **Milestones**: Milestones are cached per session to improve performance
5. **Exports**: Use "Save to Exports Folder" for local archiving
6. **Logs**: Monitor the Logs tab for troubleshooting

### Filtering Strategies
- Start broad, then narrow with filters
- Use milestone filtering for sprint-specific reports
- Combine tag + milestone filters for precise queries
- Check tag/milestone summaries in Results tab

### Security Best Practices
- Change default passwords before deployment
- Use strong, unique passwords for each user
- Never commit secrets files to version control
- Regularly review user access
- Use logout when accessing from shared devices

### Performance Optimization
- Limit max test runs (100-200 for best performance)
- Use appropriate batch sizes (50 recommended)
- Clear cache when switching between different filter sets
- Close unused browser tabs to free memory

## 📞 Support

For issues or questions:
1. Check the **Logs tab** for error details
2. Review the **Troubleshooting** section above
3. Verify your configuration (`.env` or `.streamlit/secrets.toml`)
4. Check [Qase API status](https://status.qase.io/)
5. Review documentation files in this directory

- **Configuration errors**: Check both `.env` and secrets files

---

## 🎉 What's New

### Latest Updates (November 2025)

**🔐 Authentication System**
- Multi-user authentication with username/password
- Secure session management
- Logout functionality
- Configurable user credentials

**🎯 Milestone Filtering**
- Fetch and display all project milestones
- Multi-select dropdown for milestone selection
- Filter test runs by milestone(s)
- Works alongside tag filtering
- Milestone distribution summary

**🚀 Other Improvements**
- Enhanced error handling and logging
- Improved UI with better organization
- Launcher scripts for easy startup
- Comprehensive documentation
- Streamlit Cloud deployment ready

---

**Built with ❤️ using Streamlit and Qase API**

**Version**: 2.0  
**Last Updated**: November 17, 2025
