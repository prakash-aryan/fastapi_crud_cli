#!/usr/bin/env python3

import os
import sys
import time
import requests
import json
from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.table import Table
from rich.progress import Progress
from rich.rule import Rule
from rich import box
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = os.getenv("API_PORT", "8000")
API_URL = f"http://{API_HOST}:{API_PORT}/api/items"

# ASCII art banner for CRUD CLI
CRUD_CLI_BANNER = r"""
[bold magenta]
 ██████╗██████╗ ██╗   ██╗██████╗      ██████╗██╗     ██╗
██╔════╝██╔══██╗██║   ██║██╔══██╗    ██╔════╝██║     ██║
██║     ██████╔╝██║   ██║██║  ██║    ██║     ██║     ██║
██║     ██╔══██╗██║   ██║██║  ██║    ██║     ██║     ██║
╚██████╗██║  ██║╚██████╔╝██████╔╝    ╚██████╗███████╗██║
 ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝      ╚═════╝╚══════╝╚═╝
                                                                
███╗   ███╗██╗   ██╗███████╗ ██████╗ ██╗                      
████╗ ████║╚██╗ ██╔╝██╔════╝██╔═══██╗██║                      
██╔████╔██║ ╚████╔╝ ███████╗██║   ██║██║                      
██║╚██╔╝██║  ╚██╔╝  ╚════██║██║▄▄ ██║██║                      
██║ ╚═╝ ██║   ██║   ███████║╚██████╔╝███████╗                 
╚═╝     ╚═╝   ╚═╝   ╚══════╝ ╚══▀▀═╝ ╚══════╝                 
[/bold magenta]
"""

class CrudCLI:
    def __init__(self, api_port=None):
        self.console = Console()
        
        # Use custom port if provided
        API_HOST = os.getenv("API_HOST", "127.0.0.1")
        port = api_port or os.getenv("API_PORT", "8000")
        # Add trailing slash to avoid redirects
        self.api_url = f"http://{API_HOST}:{port}/api/items/"
    
    def display_welcome(self):
        """Display welcome screen with ASCII art banner"""
        os.system('clear' if os.name == 'posix' else 'cls')
        self.console.print(CRUD_CLI_BANNER)
        self.console.print(Panel("[bold magenta]Welcome to CRUD CLI[/bold magenta]", 
                                 subtitle="A FastAPI & MySQL-powered CRUD Application with CLI Interface"))
        self.console.print("🎯 [magenta]Press Enter to continue[/magenta]")
        input()
    
    def main_menu(self):
        """Display main menu and handle user choices"""
        while True:
            os.system('clear' if os.name == 'posix' else 'cls')
            self.console.print(CRUD_CLI_BANNER)
            
            table = Table(show_header=False, box=None)
            table.add_column("", style="magenta")
            table.add_column("")
            
            table.add_row("[1]", "Create New Item")
            table.add_row("[2]", "View All Items")
            table.add_row("[3]", "View Single Item")
            table.add_row("[4]", "Update Item")
            table.add_row("[5]", "Delete Item")
            table.add_row("[6]", "Exit")
            
            self.console.print(table)
            
            choice = Prompt.ask("[magenta]Select an option[/magenta]", choices=["1", "2", "3", "4", "5", "6"])
            
            if choice == "1":
                self.create_item()
            elif choice == "2":
                self.view_all_items()
            elif choice == "3":
                self.view_single_item()
            elif choice == "4":
                self.update_item()
            elif choice == "5":
                self.delete_item()
            elif choice == "6":
                self.console.print("[magenta]Thanks for using CRUD CLI![/magenta]")
                sys.exit(0)
    
    def create_item(self):
        """Create a new item"""
        os.system('clear' if os.name == 'posix' else 'cls')
        self.console.print(Panel("[bold magenta]Create New Item[/bold magenta]"))
        
        title = Prompt.ask("[magenta]Enter title[/magenta]")
        description = Prompt.ask("[magenta]Enter description[/magenta]", default="")
        completed = Confirm.ask("[magenta]Is completed?[/magenta]", default=False)
        
        item_data = {
            "title": title,
            "description": description,
            "completed": completed
        }
        
        with Progress() as progress:
            task = progress.add_task("[magenta]Creating item...", total=100)
            for i in range(101):
                time.sleep(0.01)
                progress.update(task, completed=i)
        
        try:
            response = requests.post(self.api_url, json=item_data)
            if response.status_code == 201:
                item = response.json()
                self.console.print(Panel(f"[green]Item created successfully with ID: {item['id']}[/green]"))
            else:
                self.console.print(f"[red]Error creating item: {response.status_code}[/red]")
                if response.content:
                    self.console.print(response.json())
        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")
        
        input("\nPress Enter to return to main menu...")
    
    def view_all_items(self):
        """View all items with pagination"""
        os.system('clear' if os.name == 'posix' else 'cls')
        self.console.print(Panel("[bold magenta]View All Items[/bold magenta]"))
        
        skip = 0
        limit = 10
        
        while True:
            with Progress() as progress:
                task = progress.add_task("[magenta]Loading items...", total=100)
                for i in range(101):
                    time.sleep(0.005)
                    progress.update(task, completed=i)
            
            try:
                response = requests.get(f"{self.api_url}?skip={skip}&limit={limit}")
                if response.status_code == 200:
                    items = response.json()
                    
                    if not items:
                        self.console.print("[yellow]No items found[/yellow]")
                        input("\nPress Enter to return to main menu...")
                        return
                    
                    table = Table(title="Items List", box=box.ROUNDED)
                    table.add_column("ID", style="magenta", justify="right")
                    table.add_column("Title", style="green")
                    table.add_column("Description")
                    table.add_column("Status", justify="center")
                    
                    for item in items:
                        status = "[green]✓ Completed[/green]" if item["completed"] else "[yellow]⧖ Pending[/yellow]"
                        table.add_row(
                            str(item["id"]), 
                            item["title"], 
                            item["description"] or "-", 
                            status
                        )
                    
                    self.console.print(table)
                    
                    # For pagination, we need to check if there are more items
                    if len(items) < limit:
                        # No more items
                        break
                    
                    next_page = Confirm.ask("[magenta]Next page?[/magenta]", default=True)
                    if next_page:
                        skip += limit
                        continue
                    else:
                        break
                else:
                    self.console.print(f"[red]Error retrieving items: {response.status_code}[/red]")
                    if response.content:
                        self.console.print(response.json())
                    break
            except Exception as e:
                self.console.print(f"[red]Error: {str(e)}[/red]")
                break
        
        input("\nPress Enter to return to main menu...")
    
    def view_single_item(self):
        """View a single item by ID"""
        os.system('clear' if os.name == 'posix' else 'cls')
        self.console.print(Panel("[bold magenta]View Single Item[/bold magenta]"))
        
        item_id = int(Prompt.ask("[magenta]Enter item ID[/magenta]", default="1"))
        
        with Progress() as progress:
            task = progress.add_task("[magenta]Loading item...", total=100)
            for i in range(101):
                time.sleep(0.01)
                progress.update(task, completed=i)
        
        try:
            response = requests.get(f"{self.api_url}{item_id}")
            if response.status_code == 200:
                item = response.json()
                
                status = "[green]✓ Completed[/green]" if item["completed"] else "[yellow]⧖ Pending[/yellow]"
                
                panel_content = f"""[bold magenta]ID:[/bold magenta] {item["id"]}
[bold magenta]Title:[/bold magenta] {item["title"]}
[bold magenta]Description:[/bold magenta] {item["description"] or '-'}
[bold magenta]Status:[/bold magenta] {status}"""
                
                self.console.print(Panel(panel_content, title=f"Item #{item['id']} Details"))
            else:
                self.console.print(f"[red]Error retrieving item: {response.status_code}[/red]")
                if response.content:
                    error_data = response.json()
                    self.console.print(f"[red]{error_data.get('detail', 'Unknown error')}[/red]")
        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")
        
        input("\nPress Enter to return to main menu...")
    
    def update_item(self):
        """Update an existing item"""
        os.system('clear' if os.name == 'posix' else 'cls')
        self.console.print(Panel("[bold magenta]Update Item[/bold magenta]"))
        
        item_id = int(Prompt.ask("[magenta]Enter item ID to update[/magenta]", default="1"))
        
        with Progress() as progress:
            task = progress.add_task("[magenta]Checking item...", total=100)
            for i in range(101):
                time.sleep(0.005)
                progress.update(task, completed=i)
        
        try:
            # Get current item
            response = requests.get(f"{self.api_url}{item_id}")
            if response.status_code != 200:
                self.console.print(f"[red]Item with ID {item_id} not found[/red]")
                input("\nPress Enter to return to main menu...")
                return
            
            item = response.json()
            
            # Display current values
            self.console.print(f"[bold magenta]Current Title:[/bold magenta] {item['title']}")
            self.console.print(f"[bold magenta]Current Description:[/bold magenta] {item['description'] or '-'}")
            self.console.print(f"[bold magenta]Current Status:[/bold magenta] {'Completed' if item['completed'] else 'Pending'}")
            
            # Get new values
            title = Prompt.ask("[magenta]Enter new title[/magenta]", default=item["title"])
            description = Prompt.ask("[magenta]Enter new description[/magenta]", default=item["description"] or "")
            completed = Confirm.ask("[magenta]Is completed?[/magenta]", default=item["completed"])
            
            item_data = {
                "title": title,
                "description": description,
                "completed": completed
            }
            
            with Progress() as progress:
                task = progress.add_task("[magenta]Updating item...", total=100)
                for i in range(101):
                    time.sleep(0.01)
                    progress.update(task, completed=i)
            
            update_response = requests.put(f"{self.api_url}{item_id}", json=item_data)
            if update_response.status_code == 200:
                updated_item = update_response.json()
                self.console.print(f"[green]Item {item_id} updated successfully[/green]")
            else:
                self.console.print(f"[red]Failed to update item {item_id}[/red]")
                if update_response.content:
                    error_data = update_response.json()
                    self.console.print(f"[red]{error_data.get('detail', 'Unknown error')}[/red]")
        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")
        
        input("\nPress Enter to return to main menu...")
    
    def delete_item(self):
        """Delete an existing item"""
        os.system('clear' if os.name == 'posix' else 'cls')
        self.console.print(Panel("[bold magenta]Delete Item[/bold magenta]"))
        
        item_id = int(Prompt.ask("[magenta]Enter item ID to delete[/magenta]", default="1"))
        
        # Confirm deletion
        confirm = Confirm.ask(f"[red]Are you sure you want to delete item {item_id}?[/red]", default=False)
        if not confirm:
            self.console.print("[yellow]Deletion cancelled[/yellow]")
            input("\nPress Enter to return to main menu...")
            return
        
        with Progress() as progress:
            task = progress.add_task("[magenta]Deleting item...", total=100)
            for i in range(101):
                time.sleep(0.01)
                progress.update(task, completed=i)
        
        try:
            response = requests.delete(f"{self.api_url}{item_id}")
            if response.status_code == 204:
                self.console.print(f"[green]Item {item_id} deleted successfully[/green]")
            else:
                self.console.print(f"[red]Failed to delete item {item_id}[/red]")
                if response.content:
                    error_data = response.json()
                    self.console.print(f"[red]{error_data.get('detail', 'Unknown error')}[/red]")
        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")
        
        input("\nPress Enter to return to main menu...")
    
    def run(self):
        """Run the CLI application"""
        self.display_welcome()
        self.main_menu()