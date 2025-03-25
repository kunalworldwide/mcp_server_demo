# Claude MCP Servers Collection

This repository contains a collection of Model Context Protocol (MCP) servers that extend Claude's capabilities by connecting it to external data sources and APIs. These servers allow Claude to access real-time information such as weather forecasts, movie data, and university information.

## 📋 Contents

- **Weather Server**: Get real-time weather forecasts and alerts using the National Weather Service API
- **TMDB Movie Server**: Access information about movies and TV shows via The Movie Database API
- **Amity University Crawler**: Extract and query information from Amity University Bengaluru's website

## 🛠️ Prerequisites

Before setting up these MCP servers, make sure you have the following installed:

- **Python 3.10+**
- **Git**
- **uv** - A fast Python package installer and resolver

```
UV installation --> https://docs.astral.sh/uv/getting-started/installation/
```

## 🚀 Getting Started

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/kunalworldwide/mcp_server_demo.git

# Navigate to the project directory
cd mcp_server_demo
```

### Step 2: Install uv (if you haven't already)

**macOS/Linux**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows**:
```bash
curl -LsSf https://astral.sh/uv/install.py | python
```

After installation, restart your terminal to ensure the `uv` command is available.

### Step 3: Set Up Each Server

#### Weather Server

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

#### TMDB Movie Server

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

#### Amity University Crawler

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

Add the following to your `claude_desktop_config.json` file:


```json
{
    "mcpServers": {
        "weather": {
            "command": "/path/to/your/uv",
            "args": [
                "--directory",
                "/absolute/path/to/claude-mcp-servers/weather",
                "run",
                "weather.py"
            ]
        },
        "tmdb": {
            "command": "/path/to/your/uv",
            "args": [
                "--directory",
                "/absolute/path/to/claude-mcp-servers/movieinfo/tmdb",
                "run",
                "tmdb.py"
            ]
        },
        "amity": {
            "command": "/path/to/your/uv",
            "args": [
                "--directory",
                "/absolute/path/to/claude-mcp-servers/amity_crawler/amitycrawler",
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

Also replace `/absolute/path/to/claude-mcp-servers` with the absolute path to where you cloned the repository.

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

## 📚 Understanding the Code Structure

### Directory Structure

```
.
├── LICENSE
├── README.md
├── amitycrawler
│   ├── README.md
│   ├── amity_crawler.py
│   ├── main.py
│   ├── pyproject.toml
│   └── uv.lock
├── movieinfo
│   └── tmdb
│       ├── README.md
│       ├── main.py
│       ├── pyproject.toml
│       ├── tmdb.py
│       └── uv.lock
└── weather
    ├── README.md
    ├── main.py
    ├── pyproject.toml
    ├── uv.lock
    └── weather.py
```

Each server follows a similar structure:

1. **Main Server File** (`weather.py`, `tmdb.py`, `amity_crawler.py`):
   - Contains tool definitions and API integration logic
   - Uses FastMCP to create and run the server

2. **Data Directory** (for amity_crawler):
   - Stores crawled and structured data
   - Persists information between server sessions

3. **Dependencies**:
   - Each server uses the MCP SDK
   - Additional libraries like httpx for API requests and BeautifulSoup for web scraping

## 🔧 Troubleshooting

If you encounter issues, try these solutions:

- **Server not showing up in Claude Desktop**:
  - Check your `claude_desktop_config.json` for syntax errors
  - Ensure the paths to your servers are absolute, not relative
  - Restart Claude Desktop completely

- **Tool calls failing**:
  - Check Claude's logs for errors
  - Verify your server builds and runs without errors 
  - Make sure you've added any required API keys

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