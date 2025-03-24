from typing import Any, List, Optional
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("tmdb")

# Constants
TMDB_API_BASE = "https://api.themoviedb.org/3"
API_KEY = "<TMDB API KEY>"  # Replace with your actual API key

# Helper function for API requests
async def make_tmdb_request(endpoint: str, params: dict = None) -> dict[str, Any] | None:
    """Make a request to the TMDB API with proper error handling."""
    if params is None:
        params = {}
    
    # Add API key to all requests
    params["api_key"] = API_KEY
    
    url = f"{TMDB_API_BASE}{endpoint}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error making request to {url}: {str(e)}")
            return None

# Format movie data into readable text
def format_movie(movie: dict) -> str:
    """Format movie data into a readable string."""
    return f"""
Title: {movie.get('title', 'Unknown')}
Release Date: {movie.get('release_date', 'Unknown')}
Rating: {movie.get('vote_average', 'N/A')}/10 ({movie.get('vote_count', 0)} votes)
Overview: {movie.get('overview', 'No overview available')}
"""

# Format TV show data into readable text
def format_tv_show(show: dict) -> str:
    """Format TV show data into a readable string."""
    return f"""
Title: {show.get('name', 'Unknown')}
First Air Date: {show.get('first_air_date', 'Unknown')}
Rating: {show.get('vote_average', 'N/A')}/10 ({show.get('vote_count', 0)} votes)
Overview: {show.get('overview', 'No overview available')}
"""

# Tool implementations
@mcp.tool()
async def search_movies(query: str, year: Optional[int] = None) -> str:
    """Search for movies by title and optionally by year.
    
    Args:
        query: Movie title to search for
        year: Optional release year to filter results
    """
    params = {"query": query}
    if year:
        params["year"] = year
        
    data = await make_tmdb_request("/search/movie", params)
    
    if not data or "results" not in data:
        return "Unable to fetch movie data or no movies found."
        
    if not data["results"]:
        return f"No movies found matching '{query}'."
        
    movies = [format_movie(movie) for movie in data["results"][:5]]  # Limit to top 5 results
    return f"Found {len(data['results'])} movies. Here are the top results:\n\n" + "\n---\n".join(movies)

@mcp.tool()
async def get_now_playing() -> str:
    """Get a list of movies currently playing in theaters."""
    data = await make_tmdb_request("/movie/now_playing")
    
    if not data or "results" not in data:
        return "Unable to fetch currently playing movies."
        
    if not data["results"]:
        return "No currently playing movies found."
        
    movies = [format_movie(movie) for movie in data["results"][:5]]  # Limit to top 5 results
    return f"Movies currently in theaters:\n\n" + "\n---\n".join(movies)

@mcp.tool()
async def get_upcoming_movies() -> str:
    """Get a list of upcoming movie releases."""
    data = await make_tmdb_request("/movie/upcoming")
    
    if not data or "results" not in data:
        return "Unable to fetch upcoming movies."
        
    if not data["results"]:
        return "No upcoming movies found."
        
    movies = [format_movie(movie) for movie in data["results"][:5]]  # Limit to top 5 results
    return f"Upcoming movie releases:\n\n" + "\n---\n".join(movies)

@mcp.tool()
async def get_popular_movies() -> str:
    """Get a list of popular movies."""
    data = await make_tmdb_request("/movie/popular")
    
    if not data or "results" not in data:
        return "Unable to fetch popular movies."
        
    if not data["results"]:
        return "No popular movies found."
        
    movies = [format_movie(movie) for movie in data["results"][:5]]  # Limit to top 5 results
    return f"Currently popular movies:\n\n" + "\n---\n".join(movies)

@mcp.tool()
async def get_movie_details(movie_id: int) -> str:
    """Get detailed information about a specific movie.
    
    Args:
        movie_id: TMDB movie ID
    """
    data = await make_tmdb_request(f"/movie/{movie_id}")
    
    if not data:
        return f"Unable to fetch details for movie ID {movie_id}."
        
    # Get additional credits information
    credits = await make_tmdb_request(f"/movie/{movie_id}/credits")
    
    # Build detailed movie info
    movie_info = f"""
Title: {data.get('title', 'Unknown')}
Original Title: {data.get('original_title', 'N/A')}
Release Date: {data.get('release_date', 'Unknown')}
Runtime: {data.get('runtime', 'N/A')} minutes
Rating: {data.get('vote_average', 'N/A')}/10 ({data.get('vote_count', 0)} votes)
Genres: {', '.join([genre['name'] for genre in data.get('genres', [])])}
Status: {data.get('status', 'Unknown')}
Budget: ${data.get('budget', 0):,}
Revenue: ${data.get('revenue', 0):,}
Languages: {', '.join([lang['english_name'] for lang in data.get('spoken_languages', [])])}
Overview: {data.get('overview', 'No overview available')}
"""
    
    # Add cast information if available
    if credits and "cast" in credits and credits["cast"]:
        cast = credits["cast"][:10]  # Top 10 cast members
        cast_info = "\nCast:\n" + "\n".join([f"- {actor['name']} as {actor.get('character', 'Unknown')}" for actor in cast])
        movie_info += cast_info
        
    # Add crew information
    if credits and "crew" in credits:
        directors = [member for member in credits["crew"] if member["job"] == "Director"]
        if directors:
            director_info = "\nDirector(s): " + ", ".join([director["name"] for director in directors])
            movie_info += director_info
            
    return movie_info

@mcp.tool()
async def search_tv_shows(query: str) -> str:
    """Search for TV shows by title.
    
    Args:
        query: TV show title to search for
    """
    params = {"query": query}
    data = await make_tmdb_request("/search/tv", params)
    
    if not data or "results" not in data:
        return "Unable to fetch TV show data or no shows found."
        
    if not data["results"]:
        return f"No TV shows found matching '{query}'."
        
    shows = [format_tv_show(show) for show in data["results"][:5]]  # Limit to top 5 results
    return f"Found {len(data['results'])} TV shows. Here are the top results:\n\n" + "\n---\n".join(shows)

@mcp.tool()
async def get_popular_tv() -> str:
    """Get a list of popular TV shows."""
    data = await make_tmdb_request("/tv/popular")
    
    if not data or "results" not in data:
        return "Unable to fetch popular TV shows."
        
    if not data["results"]:
        return "No popular TV shows found."
        
    shows = [format_tv_show(show) for show in data["results"][:5]]  # Limit to top 5 results
    return f"Currently popular TV shows:\n\n" + "\n---\n".join(shows)

# Run the server
if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')