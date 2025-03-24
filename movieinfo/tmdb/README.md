# TMDB Movie Information MCP Server

A Model Context Protocol (MCP) server that connects Claude to The Movie Database (TMDB) API, providing real-time information about movies and TV shows.

## 🎬 Features

- **Movie Search**: Search for movies by title and optionally by release year
- **Movie Details**: Get detailed information about specific movies including cast and crew
- **Discover Movies**: Find currently playing, upcoming, and popular movies
- **TV Shows**: Search for TV shows and get popular TV show listings

## 📋 Prerequisites

- Python 3.11 or higher
- `httpx` for HTTP requests
- `mcp` package for the Model Context Protocol implementation
- TMDB API key (get one for free at [https://www.themoviedb.org/settings/api](https://www.themoviedb.org/settings/api))

## 🚀 Installation

1. Create and activate a virtual environment:

```bash
# Navigate to the tmdb directory
cd movieinfo/tmdb

# Create a virtual environment
uv venv

# Activate the environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
uv pip install -r requirements.txt
```

3. Configure your API key:

Create a `.env` file in the tmdb directory with your TMDB API key:

```
TMDB_API_KEY=your_api_key_here
```

Alternatively, edit the `tmdb.py` file to replace `API_KEY = "<TMDB API KEY>"` with your actual API key, though using environment variables is more secure.

## 🛠️ Usage

### Running the Server

```bash
uv run tmdb.py
```

### Available Tools

This server provides the following tools for Claude:

#### 1. `search_movies`

Search for movies by title and optionally by release year.

**Parameters**:
- `query`: Movie title to search for (string)
- `year`: Optional release year to filter results (integer)

**Example response**:
```
Found 15 movies. Here are the top results:

Title: The Avengers
Release Date: 2012-05-04
Rating: 7.7/10 (26458 votes)
Overview: When an unexpected enemy emerges and threatens global safety and security, Nick Fury, director of the international peacekeeping agency known as S.H.I.E.L.D., finds himself in need of a team to pull the world back from the brink of disaster...

---

Title: Avengers: Endgame
Release Date: 2019-04-26
Rating: 8.3/10 (20589 votes)
Overview: After the devastating events of Avengers: Infinity War, the universe is in ruins due to the efforts of the Mad Titan, Thanos...
```

#### 2. `get_movie_details`

Get detailed information about a specific movie.

**Parameters**:
- `movie_id`: TMDB movie ID (integer)

**Example response**:
```
Title: Inception
Original Title: Inception
Release Date: 2010-07-16
Runtime: 148 minutes
Rating: 8.4/10 (30412 votes)
Genres: Action, Science Fiction, Adventure
Status: Released
Budget: $160,000,000
Revenue: $836,836,967
Languages: English, Japanese, French
Overview: Cobb, a skilled thief who commits corporate espionage by infiltrating the subconscious of his targets is offered a chance to regain his old life as payment for a task considered to be impossible...

Cast:
- Leonardo DiCaprio as Dom Cobb
- Joseph Gordon-Levitt as Arthur
- Elliot Page as Ariadne
- Tom Hardy as Eames
- Ken Watanabe as Saito

Director(s): Christopher Nolan
```

#### 3. `get_now_playing`

Get a list of movies currently playing in theaters.

**Example response**:
```
Movies currently in theaters:

Title: Dune: Part Two
Release Date: 2024-02-28
Rating: 8.4/10 (1582 votes)
Overview: Follow the mythic journey of Paul Atreides as he unites with Chani and the Fremen while on a path of revenge against the conspirators who destroyed his family...

---

Title: Kung Fu Panda 4
Release Date: 2024-03-08
Rating: 6.9/10 (457 votes)
Overview: Po is gearing up to become the spiritual leader of his Valley of Peace, but also needs someone to replace him as Dragon Warrior...
```

#### 4. `get_upcoming_movies`

Get a list of upcoming movie releases.

#### 5. `get_popular_movies`

Get a list of currently popular movies.

#### 6. `search_tv_shows`

Search for TV shows by title.

**Parameters**:
- `query`: TV show title to search for (string)

#### 7. `get_popular_tv`

Get a list of popular TV shows.

## 🔄 How It Works

1. When Claude needs movie or TV show information, it calls the appropriate tool on this server.
2. The server makes requests to the TMDB API using your API key.
3. The data is formatted into a human-readable format and returned to Claude.
4. Claude can then provide this movie information to the user.

## 🔍 Troubleshooting

- **"Unable to fetch movie data or no movies found"**: Check that your search term is correct. Try using a more general search term.
- **"Unable to fetch details for movie ID"**: The movie ID may be invalid or no longer available in the TMDB database.
- **API Key Issues**: If all requests are failing, verify that your API key is correctly set and still valid.

## 🔧 Extending the Server

You can extend this movie information server by:

1. Adding more TMDB API endpoints as new tools (e.g., movie reviews, recommendations)
2. Implementing advanced search filters
3. Adding support for TV show episodes and seasons

## 📜 License

This project is licensed under the MIT License - see the LICENSE file in the root directory for details.