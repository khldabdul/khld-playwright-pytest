# Test Cases: OMDb API

**URL**: http://www.omdbapi.com/  
**Type**: Search & Data Validation  
**Priority**: 📽️ Fourth API to implement

---

## API Key Required

Get free key at: https://www.omdbapi.com/apikey.aspx

All requests require `?apikey=YOUR_KEY`

---

## Test Suite: Search by Title

### TC-OMD-001: Search Exact Title
- **Endpoint**: `GET /?t=Inception&apikey=xxx`
- **Expected**: Status 200, movie "Inception" details

### TC-OMD-002: Search Title with Year
- **Endpoint**: `GET /?t=Batman&y=2008&apikey=xxx`
- **Expected**: "The Dark Knight" returned

### TC-OMD-003: Search Non-Existent Title
- **Endpoint**: `GET /?t=asdfjkl123&apikey=xxx`
- **Expected**: `Response: "False"`, `Error: "Movie not found!"`

---

## Test Suite: Search Query

### TC-OMD-010: Search by Keyword
- **Endpoint**: `GET /?s=Batman&apikey=xxx`
- **Expected**: Array of Batman movies/shows

### TC-OMD-011: Search with Pagination
- **Endpoint**: `GET /?s=Batman&page=2&apikey=xxx`
- **Expected**: Page 2 of results

### TC-OMD-012: Search with Type Filter
- **Endpoint**: `GET /?s=Batman&type=series&apikey=xxx`
- **Expected**: Only TV series in results

---

## Test Suite: Search by IMDb ID

### TC-OMD-020: Get by IMDb ID
- **Endpoint**: `GET /?i=tt1375666&apikey=xxx`
- **Expected**: "Inception" movie details

### TC-OMD-021: Invalid IMDb ID
- **Endpoint**: `GET /?i=tt9999999999&apikey=xxx`
- **Expected**: `Response: "False"`, error message

---

## Test Suite: Response Validation

### TC-OMD-030: Verify Full Plot
- **Endpoint**: `GET /?t=Inception&plot=full&apikey=xxx`
- **Expected**: Long plot description

### TC-OMD-031: Verify Ratings Array
- **Endpoint**: `GET /?t=The Dark Knight&apikey=xxx`
- **Expected**: `Ratings` array contains IMDb, Rotten Tomatoes, Metacritic

### TC-OMD-032: Verify Response Schema
- **Endpoint**: `GET /?t=Inception&apikey=xxx`
- **Expected**: Response contains: Title, Year, Rated, Released, Runtime, Genre, Director, Writer, Actors, Plot, Language, Country, Awards, Poster, Ratings, Metascore, imdbRating, imdbVotes, imdbID, Type, DVD, BoxOffice, Production, Website, Response

---

## Test Suite: Error Handling

### TC-OMD-040: Invalid API Key
- **Endpoint**: `GET /?t=Inception&apikey=invalid`
- **Expected**: `Response: "False"`, `Error: "Invalid API key!"`

### TC-OMD-041: Missing Required Parameters
- **Endpoint**: `GET /?apikey=xxx` (no search params)
- **Expected**: `Response: "False"`, error about missing params

---

## Test Data

| Movie | IMDb ID | Year |
|-------|---------|------|
| Inception | tt1375666 | 2010 |
| The Dark Knight | tt0468569 | 2008 |
| Pulp Fiction | tt0110912 | 1994 |
| The Matrix | tt0133093 | 1999 |
| Interstellar | tt0816692 | 2014 |

---

## API Client Methods

| Method | Description |
|--------|-------------|
| `search_by_title(title, year=None)` | Exact title search |
| `search(query, type=None, page=1)` | Keyword search |
| `get_by_id(imdb_id)` | Get by IMDb ID |
| `get_full_plot(title)` | Get with full plot |
