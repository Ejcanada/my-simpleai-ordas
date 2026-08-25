from fastapi import FastAPI, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Basic Movie API",
    description="Movies Of All Times.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MOVIE DATA
movies = [
    {
        "id": 1,
        "title": "Spider-Man: Brand New Day",
        "genre": "Action / Superhero",
        "year": 2026,
        "rating": "8.5/10",
        "director": "Destin Daniel Cretton",
        "poster": "image/spiderman.png",
        "description": "Peter Parker navigates a fresh start in New York City, balancing college life and street-level heroism under a brand new mantle."
    },
    {
        "id": 2,
        "title": "The Mandalorian & Grogu",
        "genre": "Sci-Fi / Adventure",
        "year": 2026,
        "rating": "8.7/10",
        "director": "Jon Favreau",
        "poster": "image/grogu.jpg",
        "description": "The lone bounty hunter Din Djarin and his young foundling Grogu embark on a theatrical galactic journey across the outer rim."
    },
    {
        "id": 3,
        "title": "The Odyssey",
        "genre": "Epic / Fantasy",
        "year": 2026,
        "rating": "8.9/10",
        "director": "Christopher Nolan",
        "poster": "image/odyssey.png",
        "description": "An epic cinematic adaptation following Odysseus on his treacherous ten-year journey home after the fall of Troy."
    },
    {
        "id": 4,
        "title": "Insidious: The Fear the Dark",
        "genre": "Horror / Mystery",
        "year": 2025,
        "rating": "7.8/10",
        "director": "Patrick Wilson",
        "poster": "image/insidious.jpg",
        "description": "The Lambert family faces another dark chapter as demonic forces cross over from The Further into their reality."
    },
    {
        "id": 5,
        "title": "Project Hail Mary",
        "genre": "Sci-Fi / Drama",
        "year": 2026,
        "rating": "9.1/10",
        "director": "Phil Lord & Christopher Miller",
        "poster": "image/mary.jpg",
        "description": "Ryland Grace, a lone astronaut waking up with amnesia on a starship, must use science to save Earth from an extinction-level threat."
    }
]

# HOME
@app.get("/")
def home():

    return {
        "message": "Welcome to the Basic Movie API!",
        "endpoints": [
            "/movies",
            "/movies/{id}",
            "/movies/search"
        ]
    }


# GET ALL MOVIES
@app.get("/movies")
def get_movies():

    return {
        "count": len(movies),
        "movies": movies
    }


# SEARCH MOVIES 
@app.get("/movies/search")
def search_movies( q: str = Query(..., min_length=1)):
    q = q.lower()
    results = []
    for movie in movies:
        searchable_text = (
            f"{movie['title']} "
            f"{movie['genre']} "
            f"{movie['director']} "
            f"{movie['year']}"
        ).lower()

        if q in searchable_text:
            results.append(movie)

    return {
        "query": q,
        "count": len(results),
        "results": results
    }


# GET ONE MOVIE
@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):

    for movie in movies:

        if movie["id"] == movie_id:
            return movie

    raise HTTPException(
        status_code=404,
        detail="Movie not found."
    )
