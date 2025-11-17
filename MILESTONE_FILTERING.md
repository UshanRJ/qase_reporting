# Milestone Filtering Feature

## Overview
The Qase Reporting tool now supports **milestone-based filtering** for test runs. This feature allows users to select specific milestones (e.g., sprints, releases) and retrieve only the test runs associated with those milestones.

## Features

### 1. Milestone Retrieval
- **API Method**: `QaseReporter.get_milestones()`
- Fetches all available milestones from the Qase project
- Returns list of milestone dictionaries with `id` and `title` fields
- Example milestones:
  - "IBNU Sprint 60 - IS Feature"
  - "IBNU Sprint 60 - IS+ PowerBI"

### 2. Milestone Filtering
- **API Method**: `QaseReporter.get_test_runs(milestones=[...])`
- Filter test runs by one or more milestone titles
- Uses case-insensitive matching
- Works independently or combined with tag filtering

### 3. UI Components (Streamlit)
- **Checkbox**: "Enable Milestone Filtering" in sidebar
- **Multi-select Dropdown**: Select one or more milestones
- **Auto-fetch**: Milestones are fetched automatically when filter is enabled
- **Caching**: Milestones are cached in session state to avoid repeated API calls
- **Summary Display**: Shows milestone distribution in Results tab

## Usage

### Via Streamlit Web UI
1. Open the Qase Reporting app
2. In the sidebar, check "Enable Milestone Filtering"
3. Select one or more milestones from the dropdown
4. Click "Run Report" to fetch filtered test runs

### Via Python API
```python
from qase_reporter import QaseReporter
from config import Config

# Initialize
Config.load_config()
reporter = QaseReporter(
    api_token=Config.QASE_API_TOKEN,
    project_code=Config.QASE_PROJECT_CODE
)

# Fetch milestones
milestones = reporter.get_milestones()
print(f"Found {len(milestones)} milestones")

# Filter by single milestone
runs = reporter.get_test_runs(
    limit=50,
    milestones=['IBNU Sprint 60 - IS Feature']
)

# Filter by multiple milestones
runs = reporter.get_test_runs(
    limit=50,
    milestones=[
        'IBNU Sprint 60 - IS Feature',
        'IBNU Sprint 60 - IS+ PowerBI'
    ]
)

# Combine tag and milestone filtering
runs = reporter.get_test_runs(
    limit=50,
    tags=['regression', 'smoke'],
    milestones=['IBNU Sprint 60 - IS Feature']
)
```

## Implementation Details

### Backend Changes (`qase_reporter.py`)
1. **New Method**: `get_milestones()`
   - Endpoint: `GET /milestone/{project_code}`
   - Returns list of milestones with id and title

2. **Updated Method**: `get_test_runs()`
   - New parameter: `milestones: Optional[List[str]]`
   - Filters runs client-side after API fetch
   - Logs filtering results: "Milestone filter: X → Y runs"

3. **Helper Method**: `_run_has_milestones(run, required_milestones)`
   - Checks if run's milestone matches any required milestone
   - Case-insensitive comparison
   - Handles both dict and string milestone formats

### Frontend Changes (`app.py`)
1. **Updated Function**: `fetch_test_runs()`
   - New parameter: `milestones: Optional[List[str]]`
   - Extracts milestone summary from fetched runs
   - Stores `milestone_summary` in session state

2. **New UI Section**: Milestone Filtering (sidebar)
   - Checkbox to enable/disable
   - Auto-fetch milestones on enable
   - Multi-select dropdown with all available milestones
   - Info message showing selection count

3. **Results Tab Enhancement**
   - New expander: "🎯 Milestones in Loaded Runs"
   - Displays milestone distribution table
   - Shows milestone name and run count

4. **Cache Management**
   - Clear Cache button now clears milestones
   - Clears tag_summary and milestone_summary

## Testing

### Test Script
Run `test_milestones.py` to verify functionality:
```bash
python test_milestones.py
```

### Test Results
```
✓ Found 2 milestones
✓ Milestone filtering: 13 → 1 runs (matched: 'IBNU Sprint 60 - IS Feature')
✓ Combined filtering: Tag + Milestone works correctly
```

## Compatibility
- **Works alongside tag filtering**: Both features can be used together
- **Backward compatible**: Existing code continues to work (milestones parameter is optional)
- **No breaking changes**: All existing functionality preserved

## API Endpoint Used
```
GET https://api.qase.io/v1/milestone/{project_code}
```

**Request Headers**:
```json
{
  "Token": "your-api-token",
  "Accept": "application/json"
}
```

**Response Structure**:
```json
{
  "status": true,
  "result": {
    "entities": [
      {
        "id": 1,
        "title": "IBNU Sprint 60 - IS Feature",
        "description": "...",
        "created_at": "2024-11-01T00:00:00Z",
        ...
      }
    ]
  }
}
```

## Benefits
1. **Sprint-based reporting**: Filter test runs by sprint/milestone
2. **Improved organization**: Group results by release cycles
3. **Flexible filtering**: Combine with tag filtering for precise queries
4. **Better visibility**: See milestone distribution at a glance
5. **User-friendly**: Simple multi-select interface

## Example Use Cases
1. **Sprint Reports**: Get all test results for "Sprint 60"
2. **Release Reports**: Filter by release milestone "v2.0.0"
3. **Feature Reports**: Combine feature tag + milestone filter
4. **Regression Testing**: Filter regression tests for current sprint

## Notes
- Milestones must exist in Qase project to appear in dropdown
- Filtering is case-insensitive
- Empty milestone filter means "no filter" (all runs)
- Milestone summary updates automatically when runs are fetched
