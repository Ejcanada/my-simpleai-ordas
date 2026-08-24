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
        "title": "Inception",
        "genre": "Sci-Fi",
        "year": 2010,
        "rating": "8.8/10",
        "director": "Christopher Nolan",
        "poster": "",
        "description": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea."
    },
    {
        "id": 2,
        "title": "The Dark Knight",
        "genre": "Action",
        "year": 2008,
        "rating": "9.0/10",
        "director": "Christopher Nolan",
        "poster": "",
        "description": "When the menace known as the Joker wreaks havoc and chaos on Gotham, Batman must accept one of the greatest tests."
    },
    {
        "id": 3,
        "title": "Spirited Away",
        "genre": "Animation",
        "year": 2001,
        "rating": "8.6/10",
        "director": "Hayao Miyazaki",
        "poster": "",
        "description": "During her family's move to the suburbs, a 10-year-old girl wanders into a world ruled by gods, witches, and spirits."
    },
    {
        "id": 4,
        "title": "Interstellar",
        "genre": "Sci-Fi",
        "year": 2014,
        "rating": "8.7/10",
        "director": "Christopher Nolan",
        "poster": "",
        "description": "When Earth becomes uninhabitable, a farmer and ex-NASA pilot is asked to pilot a spacecraft to find a new planet."
    },
    {
        "id": 5,
        "title": "Your Name",
        "genre": "Anime",
        "year": 2016,
        "rating": "8.4/10",
        "director": "Makoto Shinkai",
        "poster": "",
        "description": "Two strangers find themselves linked in a bizarre way. When a connection forms, will distance be the only thing to keep them apart?"
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


# SEARCH MOVIES <-- FIXED (Moved above /movies/{movie_id} so FastAPI matches search correctly)
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
