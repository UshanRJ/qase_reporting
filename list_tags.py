#!/usr/bin/env python3
"""
Utility script to list all available tags in your Qase project
Helps you discover which tags to use for filtering
"""

from qase_reporter import QaseReporter
from config import Config
from rich.console import Console
from rich.table import Table
from rich import box
from typing import cast


def main():
    """List all available tags in the project"""
    
    console = Console()
    
    console.print("\n[bold cyan]═══════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]      Qase Tag Discovery Tool           [/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════[/bold cyan]\n")
    
    try:
        Config.validate()
    except ValueError as e:
        console.print(f"[red]Configuration Error: {e}[/red]")
        return
    # Initialize reporter
    reporter = QaseReporter(
        api_token=cast(str, Config.QASE_API_TOKEN),
        project_code=Config.QASE_PROJECT_CODE
    )
    
    console.print(f"[cyan]📊 Fetching test runs from project: {Config.QASE_PROJECT_CODE}...[/cyan]\n")
    
    # Fetch all test runs
    test_runs = reporter.get_test_runs(limit=100)
    
    if not test_runs:
        console.print("[yellow]No test runs found in your project[/yellow]")
        return
    
    # Collect all tags and their usage
    tag_usage = {}
    runs_by_tag = {}
    
    for run in test_runs:
        run_title = run.get('title', 'Unknown')
        tags = run.get('tags', [])
        
        if not tags:
            # Track runs with no tags
            if 'No tags' not in tag_usage:
                tag_usage['No tags'] = 0
                runs_by_tag['No tags'] = []
            tag_usage['No tags'] += 1
            runs_by_tag['No tags'].append(run_title)
        
        for tag in tags:
            if isinstance(tag, dict):
                tag_name = tag.get('title', '')
            else:
                tag_name = str(tag)
            
            if tag_name:
                if tag_name not in tag_usage:
                    tag_usage[tag_name] = 0
                    runs_by_tag[tag_name] = []
                tag_usage[tag_name] += 1
                runs_by_tag[tag_name].append(run_title)
    
    # Display summary
    console.print(f"[green]✓ Analyzed {len(test_runs)} test runs[/green]\n")
    
    if not tag_usage:
        console.print("[yellow]No tags found in any test runs[/yellow]")
        console.print("[dim]Tip: Add tags to your test runs in Qase to enable filtering[/dim]")
        return
    
    # Create summary table
    table = Table(
        title=f"Available Tags in Project: {Config.QASE_PROJECT_CODE}",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta"
    )
    
    table.add_column("Tag Name", style="cyan", no_wrap=False)
    table.add_column("Usage Count", style="green", justify="right")
    table.add_column("Percentage", style="yellow", justify="right")
    
    # Sort by usage count (descending)
    sorted_tags = sorted(tag_usage.items(), key=lambda x: x[1], reverse=True)
    
    for tag_name, count in sorted_tags:
        percentage = (count / len(test_runs)) * 100
        table.add_row(
            tag_name,
            str(count),
            f"{percentage:.1f}%"
        )
    
    console.print(table)
    console.print()
    
    # Show example usage
    console.print("[bold cyan]💡 Example Usage:[/bold cyan]\n")
    
    # Get top 3 most used tags (excluding "No tags")
    example_tags = [tag for tag, _ in sorted_tags if tag != 'No tags'][:3]
    
    if example_tags:
        console.print("[dim]Edit main_with_tags.py and set:[/dim]")
        console.print()
        console.print(f"[yellow]# Include only specific tags:[/yellow]")
        console.print(f"INCLUDE_TAGS = {example_tags[:2]}")
        console.print()
        console.print(f"[yellow]# Or exclude specific tags:[/yellow]")
        console.print(f"EXCLUDE_TAGS = {example_tags[:1]}")
        console.print()
    
    # Detailed view option
    console.print("\n[cyan]📋 Want to see which runs have each tag?[/cyan]")
    show_details = input("Show detailed breakdown? (y/n) [default: n]: ").strip().lower()
    
    if show_details == 'y':
        console.print()
        for tag_name in sorted(tag_usage.keys()):
            if tag_name == 'No tags':
                continue
            
            console.print(f"\n[bold cyan]Tag: {tag_name}[/bold cyan] ({tag_usage[tag_name]} runs)")
            console.print("[dim]" + "─" * 60 + "[/dim]")
            
            for idx, run_title in enumerate(runs_by_tag[tag_name][:10], 1):
                console.print(f"  {idx}. {run_title}")
            
            if len(runs_by_tag[tag_name]) > 10:
                console.print(f"  [dim]... and {len(runs_by_tag[tag_name]) - 10} more[/dim]")
    
    console.print("\n[bold green]✨ Tag discovery complete![/bold green]")
    console.print("[dim]Use these tags in main_with_tags.py for filtering[/dim]\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()