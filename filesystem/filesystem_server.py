#!/usr/bin/env python3
from typing import List, Dict, Any, Optional, Tuple, Union
import os
import sys
import json
import glob
import shutil
import difflib
from datetime import datetime
from pathlib import Path
import re

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("filesystem")

# Constants
ALLOWED_DIRECTORIES = []

def init_allowed_directories():
    """Initialize the list of allowed directories from command line arguments."""
    global ALLOWED_DIRECTORIES
    
    if len(sys.argv) < 2:
        print("Usage: python filesystem_server.py <allowed-directory> [additional-directories...]", file=sys.stderr)
        sys.exit(1)
    
    ALLOWED_DIRECTORIES = [str(Path(dir_path).resolve()) for dir_path in sys.argv[1:]]
    
    # Validate that all directories exist and are accessible
    for dir_path in ALLOWED_DIRECTORIES:
        try:
            if not os.path.isdir(dir_path):
                print(f"Error: {dir_path} is not a directory", file=sys.stderr)
                sys.exit(1)
        except Exception as e:
            print(f"Error accessing directory {dir_path}: {str(e)}", file=sys.stderr)
            sys.exit(1)
    
    print(f"Allowed directories: {', '.join(ALLOWED_DIRECTORIES)}", file=sys.stderr)

# Security utilities
def validate_path(requested_path: str) -> str:
    """
    Validate that a path is within allowed directories.
    
    Args:
        requested_path: The path to validate
        
    Returns:
        The absolute path if valid
        
    Raises:
        ValueError: If the path is outside allowed directories
    """
    # Expand home directory if necessary
    if requested_path.startswith('~'):
        requested_path = os.path.expanduser(requested_path)
    
    # Get absolute path
    absolute_path = os.path.abspath(requested_path)
    
    # Check if path is within allowed directories
    is_allowed = any(absolute_path.startswith(dir_path) for dir_path in ALLOWED_DIRECTORIES)
    if not is_allowed:
        raise ValueError(f"Access denied - path outside allowed directories: {absolute_path}")
    
    # Handle symlinks by checking their real path
    try:
        real_path = os.path.realpath(absolute_path)
        is_real_path_allowed = any(real_path.startswith(dir_path) for dir_path in ALLOWED_DIRECTORIES)
        if not is_real_path_allowed:
            raise ValueError("Access denied - symlink target outside allowed directories")
        return real_path
    except FileNotFoundError:
        # For new files that don't exist yet, verify parent directory
        parent_dir = os.path.dirname(absolute_path)
        try:
            real_parent_path = os.path.realpath(parent_dir)
            is_parent_allowed = any(real_parent_path.startswith(dir_path) for dir_path in ALLOWED_DIRECTORIES)
            if not is_parent_allowed:
                raise ValueError("Access denied - parent directory outside allowed directories")
            return absolute_path
        except:
            raise ValueError(f"Parent directory does not exist: {parent_dir}")

# Helper functions
def get_file_info(file_path: str) -> Dict[str, Any]:
    """Get detailed information about a file or directory."""
    stats = os.stat(file_path)
    return {
        "size": stats.st_size,
        "created": datetime.fromtimestamp(stats.st_ctime).isoformat(),
        "modified": datetime.fromtimestamp(stats.st_mtime).isoformat(),
        "accessed": datetime.fromtimestamp(stats.st_atime).isoformat(),
        "isDirectory": os.path.isdir(file_path),
        "isFile": os.path.isfile(file_path),
        "permissions": oct(stats.st_mode)[-3:],  # Last 3 digits of the octal mode
    }

def search_files(root_path: str, pattern: str, exclude_patterns: List[str] = None) -> List[str]:
    """
    Recursively search for files and directories matching a pattern.
    
    Args:
        root_path: The directory to start searching from
        pattern: The pattern to search for (case-insensitive)
        exclude_patterns: Patterns to exclude from the search
        
    Returns:
        A list of matching file and directory paths
    """
    if exclude_patterns is None:
        exclude_patterns = []
        
    results = []
    pattern = pattern.lower()
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Check if current path should be excluded
        relative_path = os.path.relpath(dirpath, root_path)
        if any(glob.fnmatch.fnmatch(relative_path, exclude) for exclude in exclude_patterns):
            continue
            
        # Check directory names
        for dirname in dirnames[:]:  # Copy the list to avoid modification issues during iteration
            full_path = os.path.join(dirpath, dirname)
            try:
                validate_path(full_path)
                
                # Check if path matches any exclude pattern
                dir_relative_path = os.path.relpath(full_path, root_path)
                should_exclude = any(glob.fnmatch.fnmatch(dir_relative_path, pattern) for pattern in exclude_patterns)
                
                if should_exclude:
                    dirnames.remove(dirname)  # Skip this directory
                    continue
                    
                if dirname.lower().find(pattern) != -1:
                    results.append(full_path)
            except ValueError:
                dirnames.remove(dirname)  # Skip this directory and don't descend into it
                
        # Check file names
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            try:
                validate_path(full_path)
                
                # Check if path matches any exclude pattern
                file_relative_path = os.path.relpath(full_path, root_path)
                should_exclude = any(glob.fnmatch.fnmatch(file_relative_path, pattern) for pattern in exclude_patterns)
                
                if should_exclude:
                    continue
                    
                if filename.lower().find(pattern) != -1:
                    results.append(full_path)
            except ValueError:
                continue
                
    return results

def normalize_line_endings(text: str) -> str:
    """Normalize line endings to LF."""
    return text.replace('\r\n', '\n')

def create_unified_diff(original_content: str, new_content: str, filepath: str = 'file') -> str:
    """Create a unified diff between two texts."""
    original_lines = normalize_line_endings(original_content).splitlines(keepends=True)
    new_lines = normalize_line_endings(new_content).splitlines(keepends=True)
    
    diff = difflib.unified_diff(
        original_lines,
        new_lines,
        fromfile=f'a/{filepath}',
        tofile=f'b/{filepath}',
        n=3  # Context lines
    )
    
    return ''.join(diff)

def apply_file_edits(file_path: str, edits: List[Dict[str, str]], dry_run: bool = False) -> str:
    """
    Apply edits to a file.
    
    Args:
        file_path: Path to the file to edit
        edits: List of {oldText, newText} pairs
        dry_run: If True, don't actually write changes
        
    Returns:
        A unified diff showing the changes
    """
    # Read file content and normalize line endings
    with open(file_path, 'r', encoding='utf-8') as f:
        content = normalize_line_endings(f.read())
    
    # Apply edits sequentially
    modified_content = content
    for edit in edits:
        old_text = normalize_line_endings(edit['oldText'])
        new_text = normalize_line_endings(edit['newText'])
        
        # If exact match exists, use it
        if old_text in modified_content:
            modified_content = modified_content.replace(old_text, new_text)
            continue
        
        # Otherwise, try line-by-line matching with flexibility for whitespace
        old_lines = old_text.split('\n')
        content_lines = modified_content.split('\n')
        match_found = False
        
        for i in range(len(content_lines) - len(old_lines) + 1):
            potential_match = content_lines[i:i + len(old_lines)]
            
            # Compare lines with normalized whitespace
            is_match = all(
                old_line.strip() == content_line.strip()
                for old_line, content_line in zip(old_lines, potential_match)
            )
            
            if is_match:
                # Preserve original indentation of first line
                original_indent_match = re.match(r'^\s*', content_lines[i])
                original_indent = original_indent_match.group(0) if original_indent_match else ''
                
                new_lines = []
                for j, line in enumerate(new_text.split('\n')):
                    if j == 0:
                        # First line gets original indentation
                        new_lines.append(original_indent + line.lstrip())
                    else:
                        # For subsequent lines, try to preserve relative indentation
                        if j < len(old_lines):
                            old_indent_match = re.match(r'^\s*', old_lines[j])
                            old_indent = old_indent_match.group(0) if old_indent_match else ''
                            
                            new_indent_match = re.match(r'^\s*', line)
                            new_indent = new_indent_match.group(0) if new_indent_match else ''
                            
                            if old_indent and new_indent:
                                relative_indent = max(0, len(new_indent) - len(old_indent))
                                new_lines.append(original_indent + ' ' * relative_indent + line.lstrip())
                            else:
                                new_lines.append(line)
                        else:
                            new_lines.append(line)
                
                content_lines[i:i + len(old_lines)] = new_lines
                modified_content = '\n'.join(content_lines)
                match_found = True
                break
        
        if not match_found:
            raise ValueError(f"Could not find exact match for edit:\n{edit['oldText']}")
    
    # Create unified diff
    diff = create_unified_diff(content, modified_content, file_path)
    
    # Format diff with appropriate number of backticks
    num_backticks = 3
    while f"{'`' * num_backticks}" in diff:
        num_backticks += 1
    
    formatted_diff = f"{'`' * num_backticks}diff\n{diff}{'`' * num_backticks}\n\n"
    
    if not dry_run:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
    
    return formatted_diff

# Tool implementations
@mcp.tool()
async def read_file(path: str) -> str:
    """Read the complete contents of a file from the file system.
    
    Handles various text encodings and provides detailed error messages
    if the file cannot be read. Use this tool when you need to examine
    the contents of a single file. Only works within allowed directories.
    
    Args:
        path: Path to the file to read
    """
    try:
        valid_path = validate_path(path)
        with open(valid_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        raise ValueError(f"Error reading file: {str(e)}")

@mcp.tool()
async def read_multiple_files(paths: List[str]) -> str:
    """Read the contents of multiple files simultaneously.
    
    This is more efficient than reading files one by one when you need to analyze
    or compare multiple files. Each file's content is returned with its
    path as a reference. Failed reads for individual files won't stop
    the entire operation. Only works within allowed directories.
    
    Args:
        paths: List of file paths to read
    """
    results = []
    
    for file_path in paths:
        try:
            valid_path = validate_path(file_path)
            with open(valid_path, 'r', encoding='utf-8') as f:
                content = f.read()
            results.append(f"{file_path}:\n{content}\n")
        except Exception as e:
            results.append(f"{file_path}: Error - {str(e)}")
    
    return "\n---\n".join(results)

@mcp.tool()
async def write_file(path: str, content: str) -> str:
    """Create a new file or completely overwrite an existing file with new content.
    
    Use with caution as it will overwrite existing files without warning.
    Handles text content with proper encoding. Only works within allowed directories.
    
    Args:
        path: Path where the file should be written
        content: Content to write to the file
    """
    try:
        valid_path = validate_path(path)
        with open(valid_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        raise ValueError(f"Error writing file: {str(e)}")

@mcp.tool()
async def edit_file(path: str, edits: List[Dict[str, str]], dry_run: bool = False) -> str:
    """Make line-based edits to a text file.
    
    Each edit replaces exact line sequences with new content.
    Returns a git-style diff showing the changes made.
    Only works within allowed directories.
    
    Args:
        path: Path to the file to edit
        edits: List of edits, each containing 'oldText' and 'newText'
        dry_run: If True, preview changes without applying them
    """
    try:
        valid_path = validate_path(path)
        result = apply_file_edits(valid_path, edits, dry_run)
        return result
    except Exception as e:
        raise ValueError(f"Error editing file: {str(e)}")

@mcp.tool()
async def create_directory(path: str) -> str:
    """Create a new directory or ensure a directory exists.
    
    Can create multiple nested directories in one operation.
    If the directory already exists, this operation will succeed silently.
    Perfect for setting up directory structures for projects or ensuring 
    required paths exist. Only works within allowed directories.
    
    Args:
        path: Path to the directory to create
    """
    try:
        valid_path = validate_path(path)
        os.makedirs(valid_path, exist_ok=True)
        return f"Successfully created directory {path}"
    except Exception as e:
        raise ValueError(f"Error creating directory: {str(e)}")

@mcp.tool()
async def list_directory(path: str) -> str:
    """Get a detailed listing of all files and directories in a specified path.
    
    Results clearly distinguish between files and directories with [FILE] and [DIR]
    prefixes. This tool is essential for understanding directory structure and
    finding specific files within a directory. Only works within allowed directories.
    
    Args:
        path: Path to the directory to list
    """
    try:
        valid_path = validate_path(path)
        entries = os.listdir(valid_path)
        formatted = []
        
        for entry in entries:
            full_path = os.path.join(valid_path, entry)
            if os.path.isdir(full_path):
                formatted.append(f"[DIR] {entry}")
            else:
                formatted.append(f"[FILE] {entry}")
        
        return "\n".join(formatted)
    except Exception as e:
        raise ValueError(f"Error listing directory: {str(e)}")

@mcp.tool()
async def directory_tree(path: str) -> str:
    """Get a recursive tree view of files and directories as a JSON structure.
    
    Each entry includes 'name', 'type' (file/directory), and 'children' for directories.
    Files have no children array, while directories always have a children array (which may be empty).
    The output is formatted with 2-space indentation for readability. 
    Only works within allowed directories.
    
    Args:
        path: Path to the directory to get the tree for
    """
    try:
        valid_path = validate_path(path)
        
        def build_tree(current_path):
            entries = []
            for item in os.listdir(current_path):
                full_path = os.path.join(current_path, item)
                try:
                    validate_path(full_path)
                    entry = {
                        "name": item,
                        "type": "directory" if os.path.isdir(full_path) else "file"
                    }
                    
                    if os.path.isdir(full_path):
                        entry["children"] = build_tree(full_path)
                    
                    entries.append(entry)
                except ValueError:
                    # Skip paths that aren't allowed
                    continue
            
            return entries
        
        tree_data = build_tree(valid_path)
        return json.dumps(tree_data, indent=2)
    except Exception as e:
        raise ValueError(f"Error building directory tree: {str(e)}")

@mcp.tool()
async def move_file(source: str, destination: str) -> str:
    """Move or rename files and directories.
    
    Can move files between directories and rename them in a single operation.
    If the destination exists, the operation will fail. Works across different
    directories and can be used for simple renaming within the same directory.
    Both source and destination must be within allowed directories.
    
    Args:
        source: Path to the file or directory to move
        destination: Path where the file or directory should be moved to
    """
    try:
        valid_source = validate_path(source)
        valid_dest = validate_path(destination)
        
        shutil.move(valid_source, valid_dest)
        return f"Successfully moved {source} to {destination}"
    except Exception as e:
        raise ValueError(f"Error moving file: {str(e)}")

@mcp.tool()
async def search_files(path: str, pattern: str, exclude_patterns: List[str] = None) -> str:
    """Recursively search for files and directories matching a pattern.
    
    Searches through all subdirectories from the starting path. The search
    is case-insensitive and matches partial names. Returns full paths to all
    matching items. Great for finding files when you don't know their exact location.
    Only searches within allowed directories.
    
    Args:
        path: Path to start the search from
        pattern: Pattern to search for (case-insensitive)
        exclude_patterns: Patterns to exclude from the search
    """
    try:
        valid_path = validate_path(path)
        results = search_files(valid_path, pattern, exclude_patterns or [])
        return "\n".join(results) if results else "No matches found"
    except Exception as e:
        raise ValueError(f"Error searching files: {str(e)}")

@mcp.tool()
async def get_file_info(path: str) -> str:
    """Retrieve detailed metadata about a file or directory.
    
    Returns comprehensive information including size, creation time, last modified time,
    permissions, and type. This tool is perfect for understanding file characteristics
    without reading the actual content. Only works within allowed directories.
    
    Args:
        path: Path to the file or directory
    """
    try:
        valid_path = validate_path(path)
        info = get_file_info(valid_path)
        
        formatted = []
        for key, value in info.items():
            formatted.append(f"{key}: {value}")
        
        return "\n".join(formatted)
    except Exception as e:
        raise ValueError(f"Error getting file info: {str(e)}")

@mcp.tool()
async def list_allowed_directories() -> str:
    """Returns the list of directories that this server is allowed to access.
    
    Use this to understand which directories are available before trying to access files.
    """
    return f"Allowed directories:\n{chr(10).join(ALLOWED_DIRECTORIES)}"

if __name__ == "__main__":
    # Initialize allowed directories from command line arguments
    init_allowed_directories()
    
    # Run the server
    print("Secure MCP Filesystem Server running", file=sys.stderr)
    mcp.run(transport='stdio')