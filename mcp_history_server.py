#!/usr/bin/env python3
# MIT License
# Copyright (c) 2023 MCP Command History Contributors
# See LICENSE file for full license text.

import os
import re
from datetime import datetime
from typing import Dict, List, Optional

from mcp.server.fastmcp import FastMCP

class HistoryManager:
    def __init__(self, hist_file: str):
        self.hist_file = os.path.expanduser(hist_file)
        self.commands = []
        self.load_history()
        
    def load_history(self):
        """Load command history from the history file."""
        if not os.path.exists(self.hist_file):
            print(f"History file not found: {self.hist_file}")
            return
            
        with open(self.hist_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        # Different shells have different history file formats
        # This handles basic formats like bash and zsh
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
                
            # Handle timestamp format in some history files (like bash with HISTTIMEFORMAT)
            timestamp_match = re.match(r'#(\d+)$', line)
            if timestamp_match:
                continue
                
            # Skip comments and metadata
            if line.startswith('#'):
                continue
                
            self.commands.append({
                "id": i,
                "command": line,
                "timestamp": datetime.now().isoformat()  # Fallback timestamp
            })
            
        print(f"Loaded {self.commands} commands from history")
        
    def search_commands(self, query: str) -> List[Dict]:
        """Search for commands matching the query."""
        if not query:
            return self.commands[-50:]  # Return most recent commands if no query
            
        results = []
        for cmd in self.commands:
            if query.lower() in cmd["command"].lower():
                results.append(cmd)
                
        return results
        
    def get_recent_commands(self, limit: int = 10) -> List[Dict]:
        """Get the most recent commands."""
        return self.commands[-limit:]
        
    def get_command(self, command_id: int) -> Optional[Dict]:
        """Get a specific command by ID."""
        for cmd in self.commands:
            if cmd["id"] == command_id:
                return cmd
        return None

# Create an MCP server
mcp = FastMCP("Shell History Explorer")

# Initialize history manager
history_manager = None

@mcp.resource("history://recent/{limit}")
def get_recent_history(limit: int) -> str:
    """Get the most recent commands from history"""
    if not history_manager:
        return "History manager not initialized"
    
    commands = history_manager.get_recent_commands(int(limit))
    result = "Recent commands:\n\n"
    for cmd in commands:
        result += f"[{cmd['id']}] {cmd['command']}\n"
    
    return result

@mcp.resource("history://search/{query}")
def search_history(query: str) -> str:
    """Search for commands in history"""
    if not history_manager:
        return "History manager not initialized"
    
    commands = history_manager.search_commands(query)
    result = f"Search results for '{query}':\n\n"
    if not commands:
        result += "No matching commands found."
    else:
        for cmd in commands:
            result += f"[{cmd['id']}] {cmd['command']}\n"
    
    return result

@mcp.tool()
def search_commands(query: str) -> List[Dict]:
    """
    Search for commands in shell history
    
    Args:
        query: Search term to find in command history
        
    Returns:
        List of matching commands with their IDs
    """
    if not history_manager:
        return []
    
    return history_manager.search_commands(query)

@mcp.tool()
def get_recent_commands(limit: int = 10) -> List[Dict]:
    """
    Get the most recent commands from history
    
    Args:
        limit: Maximum number of commands to return
        
    Returns:
        List of recent commands with their IDs
    """
    if not history_manager:
        return []
    
    return history_manager.get_recent_commands(limit)

@mcp.tool()
def get_command(command_id: int) -> Optional[Dict]:
    """
    Get a specific command by ID
    
    Args:
        command_id: ID of the command to retrieve
        
    Returns:
        Command details if found, None otherwise
    """
    if not history_manager:
        return None
    
    return history_manager.get_command(command_id)

@mcp.prompt()
def search_history_prompt(query: str) -> str:
    """Create a prompt to search command history"""
    return f"""Please search my command history for '{query}' and show me the results.
    
You can use the search_commands tool to find matching commands.
"""

@mcp.prompt()
def recent_history_prompt() -> str:
    """Create a prompt to show recent command history"""
    return """Please show me my most recent shell commands.
    
You can use the get_recent_commands tool to retrieve my command history.
"""

# Get history file path from environment variable with fallback
hist_file = os.environ.get("HISTFILE", "~/.bash_history")
history_manager = HistoryManager(hist_file)
