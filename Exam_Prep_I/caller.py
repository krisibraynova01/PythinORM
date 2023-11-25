import os
import django
from django.db.models import Q, Count, Avg, Max, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Director, Movie, Actor


# Create and run your queries within functions
def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ""

    all_directors = []

    if search_name is None:
        all_directors = Director.objects.filter(
            Q(nationality__icontains=search_nationality)
        ).order_by('full_name')

    elif search_nationality is None:
        all_directors = Director.objects.filter(
            full_name__icontains=search_name
        ).order_by('full_name')

    else:
        all_directors = Director.objects.filter(
            Q(full_name__icontains=search_name)
            &
            Q(nationality__icontains=search_nationality)
        ).order_by('full_name')

    return "\n".join(f"Director: {d.full_name}, nationality: {d.nationality}, experience: {d.years_of_experience}"
                     for d in all_directors)


def get_top_director():
    top_director = Director.objects.get_directors_by_movies_count().first()
    if not top_director:
        return ""

    return f"Top Director: {top_director.full_name}, movies: {top_director.total_movies}."


def get_top_actor():
    top_actor = Actor.objects.annotate(total_starring_movies=Count('starring_actor_movies'),
                                       average_rating=Avg('starring_actor_movies__rating')
                                       ).order_by('-total_starring_movies', 'full_name').first()

    if not top_actor or not top_actor.total_starring_movies:
        return ""

    movies = ', '.join([m.title for m in top_actor.starring_actor_movies.all()])

    return f"Top Actor: {top_actor.full_name}, starring in movies: {movies}, movies average rating: {top_actor.average_rating:.1f}"


def get_actors_by_movies_count():
    top_three_actors = Actor.objects.annotate(
        count_movies=Count('actor_movies')
    ).filter(count_movies__gt=0).order_by('-count_movies', 'full_name')[:3]

    if not top_three_actors:
        return ""

    return "\n".join(f"{a.full_name}, participated in {a.count_movies} movies" for a in top_three_actors)


def get_top_rated_awarded_movie():
    movie = Movie.objects.filter(is_awarded=True).order_by('-rating', 'title').first()

    if not movie:
        return ""

    starring_actor = movie.starring_actor.full_name if movie.starring_actor else 'N/A'
    casts = ', '.join(a.full_name for a in movie.actors.order_by('full_name'))
    return f"Top rated awarded movie: {movie.title}, rating: {movie.rating}. Starring actor: {starring_actor}. Cast: {casts}."


def increase_rating():
    movies = Movie.objects.filter(is_classic=True, rating__lt=10)

    if not movies:
        return "No ratings increased."

    updated_movies = movies.update(rating=F('rating') + 0.1)
    return f"Rating increased for {updated_movies} movies."
