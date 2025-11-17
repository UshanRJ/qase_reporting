#!/usr/bin/env python3
"""
Qase Reporter - Web UI
A modern Streamlit-based interface for the Qase Test Run Reporter
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os
import io
from typing import Optional, List, cast
import traceback

from qase_reporter import QaseReporter
from config import Config
from auth import check_multi_user_password


# Page configuration
st.set_page_config(
    page_title="Qase Test Reporter",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


def init_session_state():
    """Initialize session state variables"""
    if 'test_runs' not in st.session_state:
        st.session_state.test_runs = None
    if 'test_results' not in st.session_state:
        st.session_state.test_results = None
    if 'aggregated_df' not in st.session_state:
        st.session_state.aggregated_df = None
    if 'reporter' not in st.session_state:
        st.session_state.reporter = None
    if 'execution_logs' not in st.session_state:
        st.session_state.execution_logs = []


def add_log(message: str, level: str = "info"):
    """Add a log message to execution logs"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.execution_logs.append({
        'timestamp': timestamp,
        'level': level,
        'message': message
    })


def display_logs():
    """Display execution logs in a styled container"""
    if st.session_state.execution_logs:
        st.subheader("📋 Execution Logs")
        log_container = st.container()
        with log_container:
            for log in st.session_state.execution_logs[-20:]:  # Show last 20 logs
                if log['level'] == 'error':
                    st.error(f"[{log['timestamp']}] {log['message']}")
                elif log['level'] == 'warning':
                    st.warning(f"[{log['timestamp']}] {log['message']}")
                elif log['level'] == 'success':
                    st.success(f"[{log['timestamp']}] {log['message']}")
                else:
                    st.info(f"[{log['timestamp']}] {log['message']}")


def validate_config() -> bool:
    """Validate configuration and display errors"""
    try:
        Config.validate()
        return True
    except ValueError as e:
        st.error(f"❌ Configuration Error: {e}")
        st.info("""
        **Setup Instructions:**
        1. Create a `.env` file in the project directory
        2. Add the following variables:
           ```
           QASE_API_TOKEN=your_token_here
           QASE_PROJECT_CODE=your_project_code
           ```
        3. Restart the application
        """)
        return False


def initialize_reporter() -> Optional[QaseReporter]:
    """Initialize the Qase Reporter"""
    try:
        # Read config values and ensure they are present
        token = Config.QASE_API_TOKEN
        project = Config.PROJECT_CODE

        if not token or not project:
            add_log("✗ Missing API token or project code in configuration", "error")
            st.error("Missing API token or project code in configuration")
            return None

        # Cast to str for the type-checker now that we validated presence
        reporter = QaseReporter(
            api_token=cast(str, token),
            project_code=cast(str, project)
        )
        add_log(f"✓ Reporter initialized for project: {Config.PROJECT_CODE}", "success")
        return reporter
    except Exception as e:
        add_log(f"✗ Failed to initialize reporter: {e}", "error")
        st.error(f"Failed to initialize reporter: {e}")
        return None


def fetch_test_runs(reporter: QaseReporter, limit: int, 
                    include_tags: Optional[List[str]] = None,
                    exclude_tags: Optional[List[str]] = None,
                    milestones: Optional[List[str]] = None):
    """Fetch test runs with progress indication"""
    try:
        add_log(f"Fetching test runs (limit: {limit})...", "info")
        
        with st.spinner("🔄 Fetching test runs from Qase API..."):
            test_runs = reporter.get_test_runs(
                limit=limit,
                tags=include_tags,
                exclude_tags=exclude_tags,
                milestones=milestones
            )
        
        if test_runs:
            st.session_state.test_runs = test_runs
            add_log(f"✓ Found {len(test_runs)} test runs", "success")
            
            # Display tag summary
            tag_summary = {}
            milestone_summary = {}
            for run in test_runs:
                # Process tags
                tags = run.get('tags', [])
                for tag in tags:
                    tag_name = tag.get('title', str(tag)) if isinstance(tag, dict) else str(tag)
                    tag_summary[tag_name] = tag_summary.get(tag_name, 0) + 1
                
                # Process milestones
                milestone = run.get('milestone', {})
                if milestone:
                    milestone_name = milestone.get('title', str(milestone)) if isinstance(milestone, dict) else str(milestone)
                    milestone_summary[milestone_name] = milestone_summary.get(milestone_name, 0) + 1
            
            if tag_summary:
                st.session_state.tag_summary = tag_summary
            
            if milestone_summary:
                st.session_state.milestone_summary = milestone_summary
            
            return test_runs
        else:
            add_log("⚠ No test runs found", "warning")
            st.warning("No test runs found matching the criteria")
            return None
            
    except Exception as e:
        add_log(f"✗ Error fetching test runs: {e}", "error")
        st.error(f"Error fetching test runs: {e}")
        with st.expander("Show error details"):
            st.code(traceback.format_exc())
        return None


def fetch_test_results(reporter: QaseReporter, run_ids: List[int], batch_size: int = 50):
    """Fetch test results with progress indication"""
    try:
        add_log(f"Fetching test results for {len(run_ids)} runs...", "info")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Create a placeholder for the reporter's console output
        status_text.text(f"Retrieving results for {len(run_ids)} test runs...")
        
        test_results = reporter.get_test_results_by_runs(
            run_ids=run_ids,
            batch_size=batch_size
        )
        
        progress_bar.progress(100)
        status_text.empty()
        
        if test_results:
            st.session_state.test_results = test_results
            add_log(f"✓ Retrieved {len(test_results)} test results", "success")
            return test_results
        else:
            add_log("⚠ No test results found", "warning")
            st.warning("No test results found for the selected runs")
            return None
            
    except Exception as e:
        add_log(f"✗ Error fetching test results: {e}", "error")
        st.error(f"Error fetching test results: {e}")
        with st.expander("Show error details"):
            st.code(traceback.format_exc())
        return None


def aggregate_and_display_results(reporter: QaseReporter, test_results: List, test_runs: List):
    """Aggregate results and display them"""
    try:
        add_log("Aggregating test results...", "info")
        
        with st.spinner("📊 Aggregating test results..."):
            aggregated_df = reporter.aggregate_test_run_results(test_results, test_runs)
        
        if not aggregated_df.empty:
            st.session_state.aggregated_df = aggregated_df
            add_log(f"✓ Aggregated {len(aggregated_df)} test runs", "success")
            return aggregated_df
        else:
            add_log("⚠ No data after aggregation", "warning")
            st.warning("No data available after aggregation")
            return None
            
    except Exception as e:
        add_log(f"✗ Error aggregating results: {e}", "error")
        st.error(f"Error aggregating results: {e}")
        with st.expander("Show error details"):
            st.code(traceback.format_exc())
        return None


def display_summary_metrics(df: pd.DataFrame):
    """Display summary metrics in columns"""
    total_runs = len(df)
    total_tests = df['Total'].sum() if 'Total' in df.columns else 0
    total_passed = df['Passed'].sum() if 'Passed' in df.columns else 0
    total_blocked = df['Blocked'].sum() if 'Blocked' in df.columns else 0
    total_failed = df['Failed'].sum() if 'Failed' in df.columns else 0
    
    pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0

    total_blocked_rate = (total_blocked / total_tests * 100) if total_tests > 0 else 0
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("📦 Test Runs", total_runs)
    with col2:
        st.metric("🧪 Total Tests", f"{total_tests:,}")
    with col3:
        st.metric("✅ Passed", f"{total_passed:,}", 
                  delta=f"{pass_rate:.1f}%", delta_color="normal")
    with col4:
        st.metric("🚫 Blocked", f"{total_blocked:,}", 
                  delta=f"-{total_blocked_rate:.1f}%", delta_color="off")
    with col5:
        fail_rate = (total_failed / total_tests * 100) if total_tests > 0 else 0
        st.metric("❌ Failed", f"{total_failed:,}",
                  delta=f"-{fail_rate:.1f}%" if fail_rate > 0 else "Perfect!")
    with col6:
        st.metric("📊 Pass Rate", f"{pass_rate:.1f}%")


def export_to_excel(df: pd.DataFrame, filename: str) -> bytes:
    """Export DataFrame to Excel and return bytes"""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Test Run Results')
    output.seek(0)
    return output.getvalue()


def export_to_csv(df: pd.DataFrame) -> str:
    """Export DataFrame to CSV string"""
    return df.to_csv(index=False)


def main():
    """Main application"""
    init_session_state()
    
    # Authentication check - MUST be authenticated to continue
    if not check_multi_user_password():
        st.stop()  # Stop execution if not authenticated
        return
    
    # Header
    st.title("📊 Qase Test Run Reporter")
    st.markdown("### Interactive Dashboard for Test Results Analysis")
    st.divider()
    
    # Validate configuration
    if not validate_config():
        return
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        st.subheader("Project Settings")
        st.info(f"**Project:** {Config.PROJECT_CODE}")
        st.info(f"**Export Dir:** {Config.EXPORT_DIR}")
        
        st.divider()
        
        st.subheader("Fetch Options")
        limit = st.slider("Max Test Runs", min_value=10, max_value=500, value=100, step=10)
        batch_size = st.slider("Batch Size", min_value=10, max_value=100, value=50, step=10)
        
        st.divider()
        
        st.subheader("🏷️ Tag Filtering")
        use_tag_filter = st.checkbox("Enable Tag Filtering", value=False)
        
        include_tags = None
        exclude_tags = None
        
        if use_tag_filter:
            filter_mode = st.radio("Filter Mode", ["Include Tags", "Exclude Tags"])
            
            if filter_mode == "Include Tags":
                tags_input = st.text_input("Tags to Include (comma-separated)", 
                                          placeholder="regression, smoke")
                if tags_input:
                    include_tags = [tag.strip() for tag in tags_input.split(",")]
                    st.success(f"Will include: {include_tags}")
            else:
                tags_input = st.text_input("Tags to Exclude (comma-separated)", 
                                          placeholder="wip, draft")
                if tags_input:
                    exclude_tags = [tag.strip() for tag in tags_input.split(",")]
                    st.warning(f"Will exclude: {exclude_tags}")
        
        st.divider()
        
        # Milestone Filtering
        st.subheader("🎯 Milestone Filtering")
        use_milestone_filter = st.checkbox("Enable Milestone Filtering", value=False)
        
        selected_milestones = None
        
        if use_milestone_filter:
            # Fetch milestones if not already cached
            if 'milestones' not in st.session_state:
                with st.spinner("🔄 Fetching milestones from Qase API..."):
                    try:
                        reporter = initialize_reporter()
                        if reporter:
                            milestones = reporter.get_milestones()
                            st.session_state.milestones = milestones
                    except Exception as e:
                        st.error(f"Error fetching milestones: {e}")
                        st.session_state.milestones = []
            
            milestones = st.session_state.get('milestones', [])
            
            if milestones:
                # Extract milestone titles for dropdown
                milestone_options = [m.get('title', f"Milestone {m.get('id', 'Unknown')}") 
                                    for m in milestones]
                
                selected_milestones = st.multiselect(
                    "Select Milestones",
                    options=milestone_options,
                    placeholder="Choose one or more milestones...",
                    help="Filter test runs by the selected milestones"
                )
                
                if selected_milestones:
                    st.info(f"📍 Selected: {len(selected_milestones)} milestone(s)")
            else:
                st.warning("No milestones found in the project")
        
        st.divider()
        
        # Clear cache button
        if st.button("🗑️ Clear Cache", use_container_width=True):
            st.session_state.test_runs = None
            st.session_state.test_results = None
            st.session_state.aggregated_df = None
            st.session_state.execution_logs = []
            if 'milestones' in st.session_state:
                del st.session_state.milestones
            if 'tag_summary' in st.session_state:
                del st.session_state.tag_summary
            if 'milestone_summary' in st.session_state:
                del st.session_state.milestone_summary
            add_log("Cache cleared", "info")
            st.rerun()
    
    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs(["🚀 Execute", "📊 Results", "📋 Logs", "ℹ️ About"])
    
    with tab1:
        st.header("Execute Report Generation")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("""
            Click the button below to fetch test runs and results from Qase.
            The process will:
            1. 🔍 Fetch test runs (with optional tag and milestone filtering)
            2. 📥 Retrieve test results for each run
            3. 📊 Aggregate and display results
            """)
        
        with col2:
            if st.button("▶️ Run Report", type="primary", use_container_width=True):
                st.session_state.execution_logs = []  # Clear previous logs
                add_log("Starting report generation...", "info")
                
                # Initialize reporter
                reporter = initialize_reporter()
                if not reporter:
                    return
                
                st.session_state.reporter = reporter
                
                # Fetch test runs
                test_runs = fetch_test_runs(reporter, limit, include_tags, exclude_tags, selected_milestones)
                if not test_runs:
                    return
                
                # Extract run IDs
                run_ids = [run['id'] for run in test_runs]
                
                # Fetch test results
                test_results = fetch_test_results(reporter, run_ids, batch_size)
                if not test_results:
                    return
                
                # Aggregate and display
                aggregated_df = aggregate_and_display_results(reporter, test_results, test_runs)
                if aggregated_df is not None:
                    add_log("✅ Report generation completed successfully!", "success")
                    st.success("✅ Report generated successfully! Check the Results tab.")
                    st.balloons()
        
        st.divider()
        
        # Display current status
        if st.session_state.test_runs:
            st.success(f"✓ {len(st.session_state.test_runs)} test runs loaded")
            
            if hasattr(st.session_state, 'tag_summary') and st.session_state.tag_summary:
                with st.expander("📌 Available Tags in Loaded Runs"):
                    tag_df = pd.DataFrame([
                        {'Tag': tag, 'Count': count}
                        for tag, count in sorted(st.session_state.tag_summary.items())
                    ])
                    st.dataframe(tag_df, use_container_width=True, hide_index=True)
            
            if hasattr(st.session_state, 'milestone_summary') and st.session_state.milestone_summary:
                with st.expander("🎯 Milestones in Loaded Runs"):
                    milestone_df = pd.DataFrame([
                        {'Milestone': milestone, 'Count': count}
                        for milestone, count in sorted(st.session_state.milestone_summary.items())
                    ])
                    st.dataframe(milestone_df, use_container_width=True, hide_index=True)
        
        if st.session_state.test_results:
            st.success(f"✓ {len(st.session_state.test_results)} test results loaded")
        
        if st.session_state.aggregated_df is not None:
            st.success(f"✓ Results aggregated and ready for export")
    
    with tab2:
        st.header("Test Results")
        
        if st.session_state.aggregated_df is not None:
            df = st.session_state.aggregated_df
            
            # Summary metrics
            display_summary_metrics(df)
            
            st.divider()
            
            # Results table
            st.subheader("📋 Detailed Results")
            
            # Add search/filter
            search_term = st.text_input("🔍 Search Test Runs", placeholder="Type to filter...")
            
            if search_term:
                filtered_df = df[df['Test Run'].str.contains(search_term, case=False, na=False)]
            else:
                filtered_df = df
            
            # Display dataframe with styling
            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Test Run": st.column_config.TextColumn("Test Run", width="large"),
                    "Passed": st.column_config.NumberColumn("Passed", format="%d", help="Tests passed"),
                    "Failed": st.column_config.NumberColumn("Failed", format="%d", help="Tests failed"),
                    "Total": st.column_config.NumberColumn("Total", format="%d", help="Total tests")
                }
            )
            
            st.divider()
            
            # Export options
            st.subheader("📤 Export Options")
            
            col1, col2, col3 = st.columns(3)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            with col1:
                # Excel export
                excel_data = export_to_excel(df, f"qase_results_{timestamp}.xlsx")
                st.download_button(
                    label="📥 Download Excel",
                    data=excel_data,
                    file_name=f"qase_results_{Config.PROJECT_CODE}_{timestamp}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            with col2:
                # CSV export
                csv_data = export_to_csv(df)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name=f"qase_results_{Config.PROJECT_CODE}_{timestamp}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col3:
                # Save to exports folder
                if st.button("💾 Save to Exports Folder", use_container_width=True):
                    try:
                        # Ensure EXPORT_DIR is a valid string and directory exists
                        export_dir = Config.EXPORT_DIR or "exports"
                        os.makedirs(export_dir, exist_ok=True)

                        excel_filename = os.path.join(
                            str(export_dir),
                            f"qase_results_{Config.PROJECT_CODE}_{timestamp}.xlsx"
                        )
                        df.to_excel(excel_filename, index=False, sheet_name='Test Run Results', engine='openpyxl')
                        st.success(f"✅ Saved to: {excel_filename}")
                        add_log(f"Exported to {excel_filename}", "success")
                    except Exception as e:
                        st.error(f"❌ Error saving file: {e}")
                        add_log(f"Export failed: {e}", "error")
            
        else:
            st.info("👈 Run the report from the Execute tab to see results here")
    
    with tab3:
        st.header("Execution Logs")
        display_logs()
        
        if st.button("🗑️ Clear Logs"):
            st.session_state.execution_logs = []
            st.rerun()
    
    with tab4:
        st.header("About Qase Test Reporter")
        
        st.markdown("""
        ### 📊 Features
        - ✅ Fetch test runs from Qase API
        - 🏷️ Filter by tags (include/exclude) or milestones
        - 📊 Real-time results aggregation
        - 📈 Summary metrics and statistics
        - 📥 Export to Excel and CSV
        - 🔍 Search and filter results
        - 📋 Execution logs and error tracking
        
        ### 🚀 How to Use
        1. Configure your `.env` file with API credentials
        2. Set fetch options in the sidebar
        3. Click "Run Report" in the Execute tab
        4. View results in the Results tab
        5. Export data using download buttons
        
        ### 📝 Configuration
        Create a `.env` file with:
        ```
        QASE_API_TOKEN=your_token_here
        QASE_PROJECT_CODE=your_project_code
        EXPORT_DIR=exports
        ```
        
        ### 🔗 Resources
        - [Qase API Documentation](https://developers.qase.io/)
        - [Streamlit Documentation](https://docs.streamlit.io/)
        
        ### 📦 Version
        - Application: v2.0.0
        - Project: {project}
        """.format(project=Config.PROJECT_CODE))
        
        st.divider()
        
        st.markdown("**Built with ❤️ using Streamlit and Qase API**")


if __name__ == "__main__":
    main()
