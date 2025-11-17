#!/usr/bin/env python3
"""
Qase Test Run Reporter - Enhanced with Tag Filtering
Retrieves test run results from Qase API with tag-based filtering
"""

import requests
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich import box
import time
import sys
import html


class QaseReporter:
    """Main class to interact with Qase API and generate reports"""
    
    BASE_URL = "https://api.qase.io/v1"
    
    def __init__(self, api_token: str, project_code: str, timeout: int = 120, max_retries: int = 3):
        """
        Initialize Qase Reporter
        
        Args:
            api_token: Your Qase API token
            project_code: Project code (e.g., 'ISP', 'DEMO')
            timeout: Request timeout in seconds (default: 120)
            max_retries: Maximum number of retry attempts (default: 3)
        """
        self.api_token = api_token
        self.project_code = project_code
        self.timeout = timeout
        self.max_retries = max_retries
        self.headers = {
            "Token": api_token,
            "Accept": "application/json"
        }
        self.console = Console()
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None, retry_count: int = 0) -> Dict:
        """
        Make API request to Qase with retry logic
        
        Args:
            endpoint: API endpoint
            params: Optional query parameters
            retry_count: Current retry attempt number
            
        Returns:
            JSON response data
        """
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout as e:
            if retry_count < self.max_retries:
                wait_time = 2 ** retry_count
                self.console.print(f"[yellow]⏱  Request timed out. Retrying in {wait_time}s... (Attempt {retry_count + 1}/{self.max_retries})[/yellow]")
                time.sleep(wait_time)
                return self._make_request(endpoint, params, retry_count + 1)
            else:
                self.console.print(f"[red]❌ Request timed out after {self.max_retries} retries[/red]")
                self.console.print(f"[yellow]💡 Try reducing the data fetch limit or increasing timeout[/yellow]")
                raise
        except requests.exceptions.HTTPError as e:
            self.console.print(f"[red]HTTP Error: {e.response.status_code}[/red]")
            if hasattr(e.response, 'text'):
                self.console.print(f"[red]Details: {e.response.text[:200]}[/red]")
            raise
        except requests.exceptions.RequestException as e:
            self.console.print(f"[red]Error making API request: {e}[/red]")
            raise
    
    def get_test_runs(self, limit: int = 100, status: Optional[str] = None, 
                     tags: Optional[List[str]] = None, exclude_tags: Optional[List[str]] = None,
                     milestones: Optional[List[str]] = None) -> List[Dict]:
        """
        Fetch test runs from Qase with optional tag and milestone filtering
        
        Args:
            limit: Maximum number of runs to fetch
            status: Filter by status (active, complete, abort)
            tags: List of tags to filter BY (include only runs with these tags)
            exclude_tags: List of tags to exclude (exclude runs with these tags)
            milestones: List of milestone titles to filter by
            
        Returns:
            List of test run data
        """
        if tags and exclude_tags:
            self.console.print("[yellow]⚠  Both tags and exclude_tags specified. Using tags (include) only.[/yellow]")
        
        filter_info = []
        if tags:
            filter_info.append(f"tags: {tags}")
        elif exclude_tags:
            filter_info.append(f"excluding tags: {exclude_tags}")
        if milestones:
            filter_info.append(f"milestones: {milestones}")
        
        if filter_info:
            self.console.print(f"[cyan]📊 Fetching test runs with {', '.join(filter_info)}...[/cyan]")
        else:
            self.console.print("[cyan]📊 Fetching test runs...[/cyan]")
        
        # Use a params dict that can accept mixed value types (ints and strings)
        params: Dict[str, object] = {"limit": limit}
        if status is not None:
            # Qase API may accept status as an int code or string; keep original type but allow mixed types
            params["status"] = status
        
        try:
            response = self._make_request(f"run/{self.project_code}", params)
            
            if response.get("status"):
                runs = response.get("result", {}).get("entities", [])
                original_count = len(runs)
                
                # Apply tag filtering if specified
                if tags:
                    runs = [run for run in runs if self._run_has_tags(run, tags)]
                    self.console.print(f"[dim]Tag filter: {original_count} → {len(runs)} runs (matched tags: {tags})[/dim]")
                    original_count = len(runs)
                elif exclude_tags:
                    runs = [run for run in runs if not self._run_has_any_tag(run, exclude_tags)]
                    self.console.print(f"[dim]Tag filter: {original_count} → {len(runs)} runs (excluded tags: {exclude_tags})[/dim]")
                    original_count = len(runs)
                
                # Apply milestone filtering if specified
                if milestones:
                    runs = [run for run in runs if self._run_has_milestones(run, milestones)]
                    self.console.print(f"[dim]Milestone filter: {original_count} → {len(runs)} runs (matched milestones: {milestones})[/dim]")
                
                self.console.print(f"[green]✓ Found {len(runs)} test runs[/green]")
                return runs
            else:
                self.console.print("[red]Failed to fetch test runs[/red]")
                return []
        except Exception as e:
            self.console.print(f"[red]Error fetching test runs: {e}[/red]")
            return []
    
    def _run_has_tags(self, run: Dict, required_tags: List[str]) -> bool:
        """
        Check if a test run has all the required tags
        
        Args:
            run: Test run dictionary
            required_tags: List of tags to check for
            
        Returns:
            True if run has all required tags
        """
        run_tags = run.get('tags', [])
        if not run_tags:
            return False
        
        # Extract tag names from tag objects
        run_tag_names = set()
        for tag in run_tags:
            if isinstance(tag, dict):
                run_tag_names.add(tag.get('title', '').lower())
            else:
                run_tag_names.add(str(tag).lower())
        
        # Check if all required tags are present
        required_tags_lower = [tag.lower() for tag in required_tags]
        return all(tag in run_tag_names for tag in required_tags_lower)
    
    def _run_has_any_tag(self, run: Dict, exclude_tags: List[str]) -> bool:
        """
        Check if a test run has any of the specified tags
        
        Args:
            run: Test run dictionary
            exclude_tags: List of tags to check for
            
        Returns:
            True if run has any of the specified tags
        """
        run_tags = run.get('tags', [])
        if not run_tags:
            return False
        
        # Extract tag names from tag objects
        run_tag_names = set()
        for tag in run_tags:
            if isinstance(tag, dict):
                run_tag_names.add(tag.get('title', '').lower())
            else:
                run_tag_names.add(str(tag).lower())
        
        # Check if any exclude tag is present
        exclude_tags_lower = [tag.lower() for tag in exclude_tags]
        return any(tag in run_tag_names for tag in exclude_tags_lower)
    
    def get_milestones(self) -> List[Dict]:
        """
        Fetch all milestones from Qase project
        
        Returns:
            List of milestone dictionaries with 'id' and 'title' keys
        """
        self.console.print("[cyan]🎯 Fetching milestones...[/cyan]")
        
        try:
            response = self._make_request(f"milestone/{self.project_code}", {"limit": 100})
            
            if response.get("status"):
                milestones = response.get("result", {}).get("entities", [])
                self.console.print(f"[green]✓ Found {len(milestones)} milestones[/green]")
                return milestones
            else:
                self.console.print("[red]Failed to fetch milestones[/red]")
                return []
        except Exception as e:
            self.console.print(f"[red]Error fetching milestones: {e}[/red]")
            return []
    
    def _run_has_milestones(self, run: Dict, required_milestones: List[str]) -> bool:
        """
        Check if a test run belongs to any of the required milestones
        
        Args:
            run: Test run dictionary
            required_milestones: List of milestone titles to check for
            
        Returns:
            True if run belongs to any required milestone
        """
        run_milestone = run.get('milestone', {})
        if not run_milestone:
            return False
        
        # Get milestone title
        milestone_title = ''
        if isinstance(run_milestone, dict):
            milestone_title = run_milestone.get('title', '').lower()
        else:
            milestone_title = str(run_milestone).lower()
        
        # Check if milestone matches any required milestone
        required_milestones_lower = [ms.lower() for ms in required_milestones]
        return milestone_title in required_milestones_lower
    
    def get_test_results_by_runs(self, run_ids: List[int], batch_size: int = 50) -> List[Dict]:
        """
        Fetch test results for specific runs (more reliable for large datasets)
        
        Args:
            run_ids: List of run IDs to fetch results for
            batch_size: Number of results per batch
            
        Returns:
            List of test result data
        """
        self.console.print(f"[cyan]📥 Fetching results for {len(run_ids)} test runs...[/cyan]")
        
        all_results = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=self.console
        ) as progress:
            task = progress.add_task("Processing runs...", total=len(run_ids))
            
            for idx, run_id in enumerate(run_ids, 1):
                try:
                    progress.update(task, description=f"Fetching run {idx}/{len(run_ids)} (ID: {run_id})...")
                    
                    offset = 0
                    while True:
                        params = {
                            "limit": batch_size,
                            "offset": offset,
                            "run": run_id
                        }
                        
                        response = self._make_request(f"result/{self.project_code}", params)
                        
                        if not response.get("status"):
                            break
                        
                        results = response.get("result", {}).get("entities", [])
                        if not results:
                            break
                        
                        all_results.extend(results)
                        offset += len(results)
                        
                        if len(results) < batch_size:
                            break
                        
                        time.sleep(0.1)  # Rate limit protection
                    
                    progress.update(task, completed=idx)
                    
                except Exception as e:
                    self.console.print(f"[yellow]⚠  Error fetching run {run_id}: {e}[/yellow]")
                    progress.update(task, completed=idx)
                    continue
        
        self.console.print(f"[green]✓ Retrieved {len(all_results)} test results from {len(run_ids)} runs[/green]")
        return all_results
    
    def aggregate_test_run_results(self, test_results: List[Dict], test_runs: List[Dict]) -> pd.DataFrame:
        """
        Aggregate test results by run and status
        
        Args:
            test_results: List of test result data
            test_runs: List of test run data
            
        Returns:
            DataFrame with aggregated results
        """
        self.console.print("[cyan]🔄 Aggregating results by test run...[/cyan]")
        
        if not test_results:
            self.console.print("[yellow]No results to aggregate[/yellow]")
            return pd.DataFrame()
        
        # Create a mapping of run_id to run details
        run_mapping = {}
        for run in test_runs:
            run_id = run['id']
            run_title = run.get('title', 'Unknown Run')
            run_description = run.get('description', 'No description')
            
            # Clean description: unescape HTML entities and remove extra escaping
            if run_description and run_description != 'No description':
                # Unescape HTML entities (e.g., &nbsp;, &amp;, etc.)
                run_description = html.unescape(run_description)
                # Remove any markdown/LaTeX escaping backslashes before special chars
                run_description = run_description.replace('\\-', '-').replace('\\|', '|').replace('\\(', '(').replace('\\)', ')')
            
            run_tags = run.get('tags', [])
            
            # Format tags for display
            tag_names = []
            for tag in run_tags:
                if isinstance(tag, dict):
                    tag_names.append(tag.get('title', ''))
                else:
                    tag_names.append(str(tag))
            
            run_mapping[run_id] = {
                'title': run_title,
                'description': run_description,
                'tags': ', '.join(tag_names) if tag_names else 'No tags'
            }
        
        # Create DataFrame from results
        df = pd.DataFrame(test_results)
        
        # Ensure status field exists and is normalized
        if 'status' in df.columns:
            df['status'] = df['status'].astype(str).str.lower()
        
        # Add run details
        df['run_title'] = df['run_id'].map(lambda x: run_mapping.get(x, {}).get('title', 'Unknown Run'))
        df['run_description'] = df['run_id'].map(lambda x: run_mapping.get(x, {}).get('description', 'No description'))
        df['run_tags'] = df['run_id'].map(lambda x: run_mapping.get(x, {}).get('tags', 'No tags'))
        
        # Aggregate by run and status (excluding description to prevent escaping)
        aggregated = df.groupby(['run_id', 'run_title', 'run_tags', 'status']).size().unstack(fill_value=0)
        
        # Reset index
        aggregated = aggregated.reset_index()
        
        # Add description back from mapping (prevents escaping issues)
        aggregated['run_description'] = aggregated['run_id'].map(lambda x: run_mapping.get(x, {}).get('description', 'No description'))
        
        # Calculate total
        status_columns = [col for col in aggregated.columns if col not in ['run_id', 'run_title', 'run_description', 'run_tags']]
        aggregated['Total'] = aggregated[status_columns].sum(axis=1)
        
        # Ensure standard status columns exist
        standard_statuses = ['passed', 'failed', 'blocked', 'skipped', 'invalid', 'in_progress']
        for status in standard_statuses:
            if status not in aggregated.columns:
                aggregated[status] = 0
        
        # Reorder columns
        existing_statuses = [s for s in standard_statuses if s in aggregated.columns]
        column_order = ['run_title', 'run_description', 'run_tags'] + existing_statuses + ['Total']
        column_order = [col for col in column_order if col in aggregated.columns]
        aggregated = aggregated[column_order]
        
        # Rename columns
        aggregated = aggregated.rename(columns={
            'run_title': 'Test Run',
            'run_description': 'Description',
            'run_tags': 'Tags',
            'passed': 'Passed',
            'failed': 'Failed',
            'blocked': 'Blocked',
            'skipped': 'Skipped',
            'invalid': 'Invalid',
            'in_progress': 'In Progress'
        })
        
        self.console.print(f"[green]✓ Aggregated {len(aggregated)} test runs[/green]")
        return aggregated
    
    def display_results_table(self, df: pd.DataFrame, title: str = "Test Run Results Summary", truncate_description: int = 200):
        """
        Display results in a rich table
        
        Args:
            df: DataFrame with results
            title: Table title
            truncate_description: Maximum length for description (default: 200, 0 to disable)
        """
        if df.empty:
            self.console.print("[yellow]No data to display[/yellow]")
            return
        
        # Create a copy for display to avoid modifying original
        display_df = df.copy()
        
        # Truncate description if needed
        if truncate_description > 0 and 'Description' in display_df.columns:
            display_df['Description'] = display_df['Description'].apply(
                lambda x: (str(x)[:truncate_description] + '...') if len(str(x)) > truncate_description else str(x)
            )
        
        # Create rich table
        table = Table(
            title=title,
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta",
            title_style="bold cyan"
        )
        
        # Add columns
        for column in display_df.columns:
            if column == 'Test Run':
                table.add_column(column, style="cyan", no_wrap=False, width=40)
            elif column == 'Description':
                table.add_column(column, style="white", no_wrap=False, width=50)
            elif column == 'Tags':
                table.add_column(column, style="dim", no_wrap=False, width=20)
            elif column in ['Passed']:
                table.add_column(column, style="green", justify="right")
            elif column in ['Failed']:
                table.add_column(column, style="red", justify="right")
            elif column in ['Blocked']:
                table.add_column(column, style="yellow", justify="right")
            elif column == 'Total':
                table.add_column(column, style="bold blue", justify="right")
            else:
                table.add_column(column, justify="right")
        
        # Add rows
        for _, row in display_df.iterrows():
            table.add_row(*[str(val) for val in row.tolist()])
        
        self.console.print()
        self.console.print(table)
        self.console.print()
    
    def export_to_excel(self, df: pd.DataFrame, filename: str):
        """Export DataFrame to Excel"""
        if df.empty:
            self.console.print("[yellow]No data to export[/yellow]")
            return
        
        try:
            df.to_excel(filename, index=False, sheet_name='Test Run Results', engine='openpyxl')
            self.console.print(f"[green]✓ Exported to Excel: {filename}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error exporting to Excel: {e}[/red]")
    
    def export_to_csv(self, df: pd.DataFrame, filename: str):
        """Export DataFrame to CSV"""
        if df.empty:
            self.console.print("[yellow]No data to export[/yellow]")
            return
        
        try:
            df.to_csv(filename, index=False)
            self.console.print(f"[green]✓ Exported to CSV: {filename}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error exporting to CSV: {e}[/red]")