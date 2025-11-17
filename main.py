#!/usr/bin/env python3
"""
Main entry point for Qase Reporter with Tag Filtering
Supports filtering test runs by tags before fetching results
"""

from qase_reporter import QaseReporter
from config import Config
from datetime import datetime
import os
import sys


def main():
    """Main function with tag filtering support"""
    
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("\nPlease create a .env file with:")
        print("  QASE_API_TOKEN=your_token_here")
        print("  QASE_PROJECT_CODE=your_project_code")
        return
    
    # Initialize reporter
    # Ensure required config values are present (Config.validate() should have run earlier)
    assert Config.QASE_API_TOKEN is not None, "QASE_API_TOKEN must be set"
    assert Config.PROJECT_CODE is not None, "QASE_PROJECT_CODE must be set"
    reporter = QaseReporter(
        api_token=Config.QASE_API_TOKEN,
        project_code=Config.PROJECT_CODE,
        timeout=120,
        max_retries=3
    )
    
    reporter.console.print("\n[bold cyan]═══════════════════════════════════════[/bold cyan]")
    reporter.console.print("[bold cyan]    Qase Test Run Results Reporter    [/bold cyan]")
    reporter.console.print("[bold cyan]        With Tag Filtering Support      [/bold cyan]")
    reporter.console.print("[bold cyan]═══════════════════════════════════════[/bold cyan]\n")
    
    # ============================================================
    # CONFIGURE TAG FILTERING HERE
    # ============================================================
    
    # Option 1: Include only runs with specific tags
    # Uncomment and modify to use:
    INCLUDE_TAGS = None  # Example: ['regression', 'smoke']
    
    # Option 2: Exclude runs with specific tags
    # Uncomment and modify to use:
    EXCLUDE_TAGS = None  # Example: ['wip', 'draft']
    
    # Option 3: Ask user interactively
    USE_INTERACTIVE = True  # Set to False to skip interactive mode
    
    # ============================================================
    
    try:
        # Interactive tag selection
        if USE_INTERACTIVE:
            reporter.console.print("[cyan]📋 Tag Filtering Options:[/cyan]")
            reporter.console.print("  1. Fetch all test runs (no filtering)")
            reporter.console.print("  2. Filter by specific tags (include)")
            reporter.console.print("  3. Exclude specific tags")
            reporter.console.print()
            
            choice = input("Select option (1-3) [default: 1]: ").strip() or "1"
            
            if choice == "2":
                tags_input = input("Enter tags to INCLUDE (comma-separated): ").strip()
                if tags_input:
                    INCLUDE_TAGS = [tag.strip() for tag in tags_input.split(",")]
                    reporter.console.print(f"[green]✓ Will filter for tags: {INCLUDE_TAGS}[/green]\n")
            elif choice == "3":
                tags_input = input("Enter tags to EXCLUDE (comma-separated): ").strip()
                if tags_input:
                    EXCLUDE_TAGS = [tag.strip() for tag in tags_input.split(",")]
                    reporter.console.print(f"[green]✓ Will exclude tags: {EXCLUDE_TAGS}[/green]\n")
            else:
                reporter.console.print("[green]✓ Fetching all test runs[/green]\n")
        
        # Fetch test runs with tag filtering
        test_runs = reporter.get_test_runs(
            limit=100,
            tags=INCLUDE_TAGS,
            exclude_tags=EXCLUDE_TAGS
        )
        
        if not test_runs:
            reporter.console.print("[yellow]❌ No test runs found![/yellow]")
            reporter.console.print("\n[cyan]Possible reasons:[/cyan]")
            reporter.console.print("  • No test runs exist in your project")
            reporter.console.print("  • No test runs match your tag filter")
            reporter.console.print("  • Check your tag names (they are case-insensitive)")
            return
        
        # Show tag summary
        reporter.console.print("\n[cyan]📊 Test Runs Summary:[/cyan]")
        tag_summary = {}
        for run in test_runs:
            tags = run.get('tags', [])
            for tag in tags:
                tag_name = tag.get('title', str(tag)) if isinstance(tag, dict) else str(tag)
                tag_summary[tag_name] = tag_summary.get(tag_name, 0) + 1
        
        if tag_summary:
            reporter.console.print(f"[dim]Available tags in filtered runs:[/dim]")
            for tag_name, count in sorted(tag_summary.items()):
                reporter.console.print(f"  • {tag_name}: {count} run(s)")
        else:
            reporter.console.print("[dim]No tags found in test runs[/dim]")
        reporter.console.print()
        
        # Extract run IDs
        run_ids = [run['id'] for run in test_runs]
        
        reporter.console.print(f"[cyan]💡 Strategy: Fetching results for {len(run_ids)} filtered test runs[/cyan]\n")
        
        # Fetch test results for filtered runs
        test_results = reporter.get_test_results_by_runs(
            run_ids=run_ids,
            batch_size=50
        )
        
        if not test_results:
            reporter.console.print("[yellow]❌ No test results found![/yellow]")
            reporter.console.print("\n[cyan]Possible reasons:[/cyan]")
            reporter.console.print("  • No test cases have been executed in filtered runs")
            reporter.console.print("  • API timeout (try reducing batch size)")
            return
        
        # Aggregate results
        aggregated_df = reporter.aggregate_test_run_results(test_results, test_runs)
        
        if aggregated_df.empty:
            reporter.console.print("[yellow]❌ No data to display after aggregation[/yellow]")
            return
        
        # Display results table
        title = f"Test Run Results Summary - Project: {Config.PROJECT_CODE}"
        if INCLUDE_TAGS:
            title += f" (Tags: {', '.join(INCLUDE_TAGS)})"
        elif EXCLUDE_TAGS:
            title += f" (Excluding: {', '.join(EXCLUDE_TAGS)})"
        
        reporter.display_results_table(aggregated_df, title=title)
        
        # Generate timestamp for filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Add tag info to filename
        tag_suffix = ""
        if INCLUDE_TAGS:
            tag_suffix = f"_tags_{'_'.join(INCLUDE_TAGS)}"
        elif EXCLUDE_TAGS:
            tag_suffix = f"_excl_{'_'.join(EXCLUDE_TAGS)}"
        
        # Export to Excel
        excel_filename = os.path.join(
            Config.EXPORT_DIR,
            f"qase_test_runs_{Config.PROJECT_CODE}{tag_suffix}_{timestamp}.xlsx"
        )
        reporter.export_to_excel(aggregated_df, excel_filename)
        
        # Export to CSV
        csv_filename = os.path.join(
            Config.EXPORT_DIR,
            f"qase_test_runs_{Config.PROJECT_CODE}{tag_suffix}_{timestamp}.csv"
        )
        reporter.export_to_csv(aggregated_df, csv_filename)
        
        reporter.console.print(f"\n[bold green]✨ Report generation complete![/bold green]")
        reporter.console.print(f"[dim]Files saved in: {Config.EXPORT_DIR}/[/dim]")
        reporter.console.print(f"[dim]Runs filtered: {len(test_runs)} | Results retrieved: {len(test_results)}[/dim]\n")
        
    except KeyboardInterrupt:
        reporter.console.print(f"\n\n[yellow]⚠  Operation cancelled by user[/yellow]\n")
    except Exception as e:
        reporter.console.print(f"\n[bold red]❌ Error: {e}[/bold red]\n")
        reporter.console.print("[cyan]Troubleshooting tips:[/cyan]")
        reporter.console.print("  1. Check your internet connection")
        reporter.console.print("  2. Verify your API token is correct")
        reporter.console.print("  3. Ensure the project code is correct")
        reporter.console.print("  4. Verify tag names (case-insensitive)")
        reporter.console.print(f"  5. Check Qase API status at: https://status.qase.io/\n")
        
        import traceback
        reporter.console.print("[dim]Full error details:[/dim]")
        traceback.print_exc()


if __name__ == "__main__":
    main()