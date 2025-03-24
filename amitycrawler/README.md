# Amity University Crawler MCP Server

A Model Context Protocol (MCP) server that crawls and provides structured information from Amity University Bengaluru's website, enabling Claude to answer questions about courses, faculty, events, and admissions.

## 🎓 Features

- **Course Information**: Search and retrieve detailed information about courses offered at Amity University
- **Faculty Directory**: Access faculty information, filterable by department
- **Events Calendar**: View upcoming events at the university
- **Admissions Information**: Get details about the admission process, deadlines, and requirements
- **Data Caching**: Stores crawled data locally, reducing the need for frequent web scraping
- **Data Refresh**: On-demand refreshing of all university data

## 📋 Prerequisites

- Python 3.11 or higher
- `httpx` for HTTP requests
- `beautifulsoup4` for HTML parsing
- `mcp` package for the Model Context Protocol implementation

## 🚀 Installation

1. Create and activate a virtual environment:

```bash
# Navigate to the amity_crawler directory
cd amity_crawler

# Create a virtual environment
uv venv

# Activate the environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
uv pip install -r requirements.txt
```

## 🛠️ Usage

### Running the Server

```bash
uv run amity_crawler.py
```

### Available Tools

This server provides the following tools for Claude:

#### 1. `get_courses`

Get information about courses offered by Amity University Bengaluru.

**Parameters**:
- `query`: Optional search term to filter courses

**Example response**:
```
Found 3 courses matching 'computer':

Course: B.Tech in Computer Science
Duration: 4 years
Description: Comprehensive computer science program

Course: M.Tech in Computer Applications
Duration: 2 years
Description: Advanced study in computer applications and systems

Course: Diploma in Computer Applications
Duration: 1 year
Description: Practical training in computer applications
```

#### 2. `get_faculty`

Get information about faculty at Amity University Bengaluru.

**Parameters**:
- `department`: Optional department name to filter faculty

**Example response**:
```
Found 2 faculty members in department 'Computer Science':

Name: Dr. Amit Kumar
Designation: Professor
Department: Computer Science
Bio: Ph.D in AI

Name: Dr. Priya Verma
Designation: Associate Professor
Department: Computer Science
Bio: Expert in Machine Learning
```

#### 3. `get_events`

Get information about upcoming events at Amity University Bengaluru.

**Example response**:
```
Upcoming events at Amity University Bengaluru:

Event: Tech Symposium 2025
Date: April 15, 2025
Description: Annual technology conference

Event: Cultural Fest
Date: May 5-7, 2025
Description: Annual cultural festival
```

#### 4. `get_admission_info`

Get information about the admission process at Amity University Bengaluru.

**Example response**:
```
Admission Process:
The admission process includes application submission, entrance test, and interview.

Application Deadlines:
- April 30, 2025 for Fall semester
- November 30, 2025 for Spring semester

Requirements:
- Completed application form
- Academic transcripts
- Entrance test scores

Fees:
- Application: ₹1500
- Tuition: Varies by program

Scholarships:
- Merit-based scholarships available
- Sports scholarships

Last Updated: 2025-03-24T12:34:56.789012
```

#### 5. `refresh_data`

Crawl the Amity University Bengaluru website to refresh all data.

**Example response**:
```
Data successfully refreshed at 2025-03-24T13:45:30.123456.

Summary of collected data:
- 15 courses
- 24 faculty members
- 5 events
- Admission information updated
```

#### 6. `get_data_status`

Get information about when the data was last refreshed.

**Example response**:
```
Data Status for Amity University Bengaluru Information:

Last data refresh: 2025-03-24T13:45:30.123456
Available information:
- Courses: 15 entries
- Faculty: 24 entries
- Events: 5 entries
- Admission information: Available

To refresh the data, use the refresh_data tool.
```

## 🔄 How It Works

1. The crawler scans the Amity University Bengaluru website and extracts structured information.
2. The extracted data is stored in JSON files within the `amity_data` directory.
3. When Claude needs university information, it calls the appropriate tool on this server.
4. The server retrieves the requested information from the cached data files.
5. If necessary, the data can be refreshed on demand with the `refresh_data` tool.

## 📂 Data Structure

The data is stored in the following structure:

```
amity_data/
├── courses.json      # Course information
├── faculty.json      # Faculty information
├── events.json       # Event information
├── admissions.json   # Admissions information
├── news.json         # University news
├── contact.json      # Contact information
├── campus.json       # Campus information
└── last_crawl.txt    # Timestamp of the last successful crawl
```

## 🔍 Troubleshooting

- **Empty or Missing Data**: Use the `refresh_data` tool to update the data cache.
- **"No results found"**: Try using more general search terms or check if the data has been recently refreshed.
- **Crawling Errors**: If the `refresh_data` tool is failing, it may be due to changes in the university website structure. Check the logs for more information.

## 🔧 Extending the Server

You can extend this university crawler by:

1. Adding support for more sections of the university website
2. Implementing more advanced search and filtering capabilities
3. Adding data validation to ensure consistency
4. Enhancing the crawler to handle more complex page structures

## 📜 License

This project is licensed under the MIT License - see the LICENSE file in the root directory for details.