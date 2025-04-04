# Claude MCP Servers Collection

This repository contains a collection of Model Context Protocol (MCP) servers that extend Claude's capabilities by connecting it to external data sources and APIs. These servers allow Claude to access real-time information such as weather forecasts, movie data, and university information.

## 📋 Contents

- **Weather Server**: Get real-time weather forecasts and alerts using the National Weather Service API
- **TMDB Movie Server**: Access information about movies and TV shows via The Movie Database API
- **Amity University Crawler**: Extract and query information from Amity University Bengaluru's website
- **Filesystem Server**: Access and manage files on your local filesystem

## 🛠️ Prerequisites

Before setting up these MCP servers, make sure you have one of the following installed:

- **Docker** (recommended for easy setup)
  - Docker Desktop for Windows/Mac or Docker Engine for Linux
  - No other dependencies needed

OR if you prefer to run without Docker:

- **Python 3.10+**
- **Git**
- **uv** - A fast Python package installer and resolver

```
UV installation --> https://docs.astral.sh/uv/getting-started/installation/
```

## 🚀 Getting Started

### Option 1: Using Docker (Recommended)

#### Step 1: Pull the Docker images

```bash
# Pull the Weather MCP server
docker pull kunalondock/mcp-weather:pythonv1

# Pull the TMDB Movie MCP server
docker pull kunalondock/mcp-movie:pythonv1

# Pull the Amity University MCP server
docker pull kunalondock/mcp-amity:pythonv1

# Pull the Filesystem MCP server
docker pull kunalondock/mcp-filesystem:pythonv1
```

#### Step 2: Configure Claude Desktop

Skip to the "Connecting to Claude Desktop" section below and use the Docker configuration.

### Option 2: Manual Setup with Python

#### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/kunalworldwide/mcp_server_demo.git

# Navigate to the project directory
cd mcp_server_demo
```

#### Step 2: Install uv (if you haven't already)

**macOS/Linux**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows**:
```bash
curl -LsSf https://astral.sh/uv/install.py | python
```

After installation, restart your terminal to ensure the `uv` command is available.

#### Step 3: Set Up Each Server

##### Weather Server

```bash
# Navigate to the weather directory
cd weather

# Create a virtual environment and activate it
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt

# Test the server
uv run weather.py
```

##### TMDB Movie Server

```bash
# Navigate to the tmdb directory
cd ../movieinfo/tmdb

# Create a virtual environment and activate it
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt

# Open tmdb.py and replace YOUR_API_KEY_HERE with your TMDB API key
# You can get a free API key at https://www.themoviedb.org/settings/api

# Test the server
uv run tmdb.py
```

##### Amity University Crawler

```bash
# Navigate to the amity_crawler directory
cd ../../amity_crawler/amitycrawler

# Create a virtual environment and activate it
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt

# Test the server
uv run amity_crawler.py
```

## 🔌 Connecting to Claude Desktop

To connect these servers to Claude Desktop, you need to configure the Claude Desktop application.

### Step 1: Open the Claude Desktop Config File

The configuration file is located at:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Roaming\Claude\claude_desktop_config.json`

Create this file if it doesn't exist.

### Step 2: Add Server Configurations

#### Option 1: Docker Configuration (Recommended)

Add the following to your `claude_desktop_config.json` file to use the pre-built Docker images:

```json
{
    "mcpServers": {
        "weather": {
            "command": "docker",
            "args": [
                "run",
                "-i",
                "--rm",
                "kunalondock/mcp-weather:pythonv1"
            ]
        },
        "tmdb": {
            "command": "docker",
            "args": [
                "run",
                "-i",
                "-e", "TMDB_API_KEY=46c00bf3aa4f426c510c4b3a026c29d6",
                "--rm",
                "kunalondock/mcp-movie:pythonv1"
            ]
        },
        "amity": {
            "command": "docker",
            "args": [
                "run",
                "-i",
                "--rm",
                "--mount", "type=volume,src=amity-data,dst=/app/amity_data",
                "kunalondock/mcp-amity:pythonv1"
            ]
        },
        "filesystem": {
            "command": "docker",
            "args": [
                "run",
                "-i",
                "--rm",
                "--mount", "type=bind,src=C:\\path\\to\\your\\files,dst=/projects/files",
                "kunalondock/mcp-filesystem:pythonv1",
                "/projects"
            ]
        }
    }
}
```

Notes:
- For the filesystem server, replace `C:\\path\\to\\your\\files` with the Windows path to the directory you want to make accessible to Claude
- On macOS/Linux, use the appropriate path format: `/path/to/your/files`
- The TMDB API key is pre-configured, but you can replace it with your own if needed

#### Option 2: Local Python Configuration

If you're not using Docker and have set up the servers locally with Python, use this configuration instead:

```json
{
    "mcpServers": {
        "weather": {
            "command": "/path/to/your/uv",
            "args": [
                "--directory",
                "/absolute/path/to/mcp_server_demo/weather",
                "run",
                "weather.py"
            ]
        },
        "tmdb": {
            "command": "/path/to/your/uv",
            "args": [
                "--directory",
                "/absolute/path/to/mcp_server_demo/movieinfo/tmdb",
                "run",
                "tmdb.py"
            ]
        },
        "amity": {
            "command": "/path/to/your/uv",
            "args": [
                "--directory",
                "/absolute/path/to/mcp_server_demo/amitycrawler",
                "run",
                "amity_crawler.py"
            ]
        }
    }
}
```

Replace `/path/to/your/uv` with the actual path to your uv executable. You can find this by running:
```bash
which uv  # On macOS/Linux
```
```powershell
(Get-Command uv).Source #On Windows
```

Also replace `/absolute/path/to/mcp_server_demo` with the absolute path to where you cloned the repository.

### Step 3: Restart Claude Desktop

After saving the configuration file, restart Claude Desktop for the changes to take effect.

## 🔍 Testing the Servers

Once connected, you can test each server by asking Claude questions like:

- **Weather Server**:
  - "What's the weather like in Sacramento?"
  - "Are there any weather alerts in Texas?"

- **TMDB Movie Server**:
  - "What movies are currently popular?"
  - "Find me information about recent sci-fi movies."
  - "What TV shows are trending now?"

- **Amity University Server**:
  - "What courses are offered at Amity University Bengaluru?"
  - "Who are the faculty members in the Computer Science department?"
  - "Tell me about the admission process at Amity University."

- **Filesystem Server**:
  - "What files are in my Downloads folder?"
  - "Read the content of file.txt"
  - "Create a new directory called 'claude-files'"

## 🔧 Troubleshooting

If you encounter issues, try these solutions:

- **Docker not running**:
  - Make sure Docker Desktop or Docker Engine is running
  - Check if you can run a simple Docker container with `docker run hello-world`

- **Docker images not found**:
  - Verify you pulled the images with `docker images | grep kunalondock`
  - If not found, run the docker pull commands again

- **Server not showing up in Claude Desktop**:
  - Check your `claude_desktop_config.json` for syntax errors
  - Ensure the paths in your configuration are correct
  - Restart Claude Desktop completely

- **Tool calls failing**:
  - Check Claude's logs for errors
  - Verify Docker can access the necessary files and directories
  - Make sure you've configured the correct paths

- **Checking Claude's logs**:
  - macOS: Check log files in `~/Library/Logs/Claude/`
  - Windows: Check log files in `%APPDATA%\Claude\Logs\`

## 🤝 Contributing

Feel free to enhance these servers or add new ones. Some ideas:
- Add more detailed weather information
- Expand the movie database to include reviews and recommendations
- Add more university information sources

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Anthropic for creating Claude and the Model Context Protocol
- The MCP documentation at [modelcontextprotocol.io](https://modelcontextprotocol.io)
- The National Weather Service and TMDB for their public APIs
- Amity University Bengaluru for educational information

---

Happy building with AI! 🚀
