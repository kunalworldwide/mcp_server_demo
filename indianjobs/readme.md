# Jobs API MCP Server

A Model Context Protocol (MCP) server that connects Claude to the Jobs API, providing real-time access to job listings from across the internet.

## 💼 Features

- **Job Search**: Search for jobs with filters for title, company, location, experience level, and job type
- **Job Details**: Get comprehensive information about specific job listings
- **Recent Jobs**: Retrieve the most recently posted job opportunities
- **API Status**: Check the status and usage information for the Jobs API

## 📋 Prerequisites

- Python 3.11 or higher
- `httpx` for HTTP requests
- `mcp` package for the Model Context Protocol implementation
- Jobs API key (get one for free at [http://indianapi.in/jobs-api](http://indianapi.in/jobs-api))

## 🚀 Installation

### Option 1: Using Docker (Recommended)

1. Build the Docker image:

```bash
# Navigate to the directory containing the Dockerfile
cd jobs_mcp_server

# Build the Docker image
docker build -t jobs-mcp-server .
```

2. Run the Docker container with your API key:

```bash
docker run -e JOBS_API_KEY=your_api_key_here jobs-mcp-server
```

### Option 2: Manual Setup

1. Create and activate a virtual environment:

```bash
# Create a virtual environment
python -m venv venv

# Activate the environment
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure your API key:

Create a `.env` file in the project directory with your Jobs API key:

```
JOBS_API_KEY=your_api_key_here
```

4. Run the server:

```bash
python jobs_server.py
```

## 🛠️ Usage with Claude Desktop

To connect this server to Claude Desktop, you need to configure the Claude Desktop application.

### Step 1: Open the Claude Desktop Config File

The configuration file is located at:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Roaming\Claude\claude_desktop_config.json`

Create this file if it doesn't exist.

### Step 2: Add the Jobs Server Configuration

Add the following to your `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "jobs": {
      "command": "docker",
      "args": [
        "run",
        "-e", "JOBS_API_KEY=your_api_key_here",
        "jobs-mcp-server"
      ]
    }
  }
}
```

Alternatively, if you prefer to run without Docker:

```json
{
  "mcpServers": {
    "jobs": {
      "command": "/path/to/python",
      "args": [
        "/absolute/path/to/jobs_server.py"
      ],
      "env": {
        "JOBS_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Step 3: Restart Claude Desktop

After saving the configuration file, restart Claude Desktop for the changes to take effect.

## 🔍 Available Tools

This server provides the following tools for Claude:

### 1. `search_jobs`

Search for job listings with optional filters.

**Parameters**:
- `limit`: Number of job listings to return (default: 10)
- `location`: Filter jobs by location (e.g., "Bangalore", "Mumbai")
- `title`: Search for jobs by title (e.g., "Software Engineer", "Data Scientist")
- `company`: Filter jobs by company (e.g., "Google", "Microsoft")
- `experience`: Filter by required experience level (e.g., "Fresher", "1-3 years")
- `job_type`: Filter by job type (e.g., "Full Time", "Part Time")

### 2. `get_job_by_id`

Get detailed information about a specific job listing.

**Parameters**:
- `job_id`: The unique identifier for the job posting

### 3. `get_recent_jobs`

Get a list of the most recently posted jobs.

**Parameters**:
- `limit`: Number of job listings to return (default: 10)

### 4. `get_api_status`

Check the status of the Jobs API and provide usage information.

## 🔄 How It Works

1. When Claude needs job information, it calls the appropriate tool on this server.
2. The server makes requests to the Jobs API using your API key.
3. The data is formatted into a human-readable format and returned to Claude.
4. Claude can then provide this job information to the user.

## 🔍 Troubleshooting

- **"Unable to fetch job listings"**: Check that your API key is correct and still valid.
- **"No job listings found matching your criteria"**: Try using broader search terms or fewer filters.
- **"The Jobs API appears to be unavailable"**: The API may be experiencing downtime. Try again later.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.