from typing import Any, Dict, List, Optional
import httpx
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("jobs")

# Constants
API_BASE_URL = "https://jobs.indianapi.in"
API_KEY = os.getenv("JOBS_API_KEY")  # Get API key from environment

# Helper function for API requests
async def make_jobs_request(endpoint: str, params: dict = None) -> dict[str, Any] | None:
    """Make a request to the Jobs API with proper error handling."""
    if params is None:
        params = {}
    
    url = f"{API_BASE_URL}{endpoint}"
    
    headers = {
        "X-Api-Key": API_KEY,
        "User-Agent": "jobs-mcp-server/1.0"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error making request to {url}: {str(e)}")
            return None

# Format job listing data into readable text
def format_job(job: dict) -> str:
    """Format job listing data into a readable string."""
    return f"""
Title: {job.get('title', 'Unknown')}
Company: {job.get('company', 'Unknown')}
Location: {job.get('location', 'Unknown')}
Job Type: {job.get('job_type', 'Unknown')}
Experience: {job.get('experience', 'Unknown')}
Posted Date: {job.get('posted_date', 'Unknown')}

Description: {job.get('job_description', 'No description available')}

Roles & Responsibilities: {job.get('role_and_responsibility', 'Not specified')}

Education & Skills: {job.get('education_and_skills', 'Not specified')}

About Company: {job.get('about_company', 'No company information available')}

Apply Link: {job.get('apply_link', 'No link available')}
"""

# Tool implementations
@mcp.tool()
async def search_jobs(
    limit: Optional[str] = "10", 
    location: Optional[str] = None,
    title: Optional[str] = None,
    company: Optional[str] = None,
    experience: Optional[str] = None,
    job_type: Optional[str] = None
) -> str:
    """Search for job listings with optional filters.
    
    Args:
        limit: Number of job listings to return (default: 10)
        location: Filter jobs by location (e.g., "Bangalore", "Mumbai")
        title: Search for jobs by title (e.g., "Software Engineer", "Data Scientist")
        company: Filter jobs by company (e.g., "Google", "Microsoft")
        experience: Filter by required experience level (e.g., "Fresher", "1-3 years")
        job_type: Filter by job type (e.g., "Full Time", "Part Time")
    """
    # Build query parameters
    params = {"limit": limit}
    if location:
        params["location"] = location
    if title:
        params["title"] = title
    if company:
        params["company"] = company
    if experience:
        params["experience"] = experience
    if job_type:
        params["job_type"] = job_type
    
    # Make API request
    data = await make_jobs_request("/jobs", params)
    
    if not data:
        return "Unable to fetch job listings. Please check your API key or try again later."
    
    if not isinstance(data, list):
        return "Unexpected response format. Expected a list of job listings."
    
    if len(data) == 0:
        return "No job listings found matching your criteria."
    
    job_count = len(data)
    displayed_count = min(job_count, int(limit))
    
    jobs_info = [format_job(job) for job in data[:displayed_count]]
    
    return f"Found {job_count} jobs. Showing {displayed_count}:\n\n" + "\n---\n".join(jobs_info)

@mcp.tool()
async def get_job_by_id(job_id: int) -> str:
    """Get detailed information about a specific job listing.
    
    Args:
        job_id: The unique identifier for the job posting
    """
    # Make API request
    data = await make_jobs_request(f"/jobs/{job_id}")
    
    if not data:
        return f"Unable to fetch job with ID {job_id}. Please check the ID or try again later."
    
    # Format the job data
    return format_job(data)

@mcp.tool()
async def get_recent_jobs(limit: Optional[str] = "10") -> str:
    """Get a list of the most recently posted jobs.
    
    Args:
        limit: Number of job listings to return (default: 10)
    """
    # Make API request
    params = {"limit": limit, "sort": "posted_date"}
    data = await make_jobs_request("/jobs", params)
    
    if not data:
        return "Unable to fetch recent job listings. Please check your API key or try again later."
    
    if not isinstance(data, list):
        return "Unexpected response format. Expected a list of job listings."
    
    if len(data) == 0:
        return "No recent job listings found."
    
    job_count = len(data)
    displayed_count = min(job_count, int(limit))
    
    jobs_info = [format_job(job) for job in data[:displayed_count]]
    
    return f"Found {job_count} recent jobs. Showing {displayed_count}:\n\n" + "\n---\n".join(jobs_info)

# Tool to provide information about API status
@mcp.tool()
async def get_api_status() -> str:
    """Check the status of the Jobs API and provide usage information."""
    # Make a simple API request to check status
    data = await make_jobs_request("/jobs", {"limit": "1"})
    
    if not data:
        return "The Jobs API appears to be unavailable at this time. Please try again later."
    
    return """
Jobs API Status: Available

Usage Information:
- The Jobs API provides access to real-time job postings aggregated from across the internet.
- You can search for jobs by title, company, location, experience level, and job type.
- For higher usage limits, consider upgrading to a paid plan at http://indianapi.in/jobs-api.

API Documentation:
- Base URL: https://jobs.indianapi.in
- Authentication: Requires API key in X-Api-Key header
- For testing: Use the sandbox environment at http://indianapi.in/sandbox/jobs-api
"""

# Run the server
if __name__ == "__main__":
    if not API_KEY:
        print("WARNING: No API key provided. Set the JOBS_API_KEY environment variable.")
        print("You can get an API key by subscribing at http://indianapi.in/jobs-api")
    
    # Initialize and run the server
    mcp.run(transport='stdio')