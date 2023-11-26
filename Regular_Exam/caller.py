import os
import django
from django.db.models import Q, Count, Avg, Sum

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Article, Review


# Create and run your queries within functions
def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ""

    all_authors = Author.objects.all()

    if search_name is None:
        all_authors = all_authors.filter(
            email__icontains=search_email
        ).order_by('-full_name')

    elif search_email is None:
        all_authors = all_authors.filter(
            full_name__icontains=search_name
        ).order_by('-full_name')

    elif search_name is not None and search_email is not None:
        all_authors = all_authors.filter(
            Q(full_name__icontains=search_name)
            &
            Q(email__icontains=search_email)
        ).order_by('-full_name')

    if not all_authors:
        return ""

    result = []
    for author in all_authors:
        status = "Banned" if author.is_banned else "Not Banned"
        result.append(f"Author: {author.full_name}, email: {author.email}, status: {status}")

    return '\n'.join(result)


def get_top_publisher():
    top_author = Author.objects.get_authors_by_article_count().filter(num_of_articles__gt=0).first()

    if not top_author or top_author.num_of_articles == 0:
        return ""

    else:

        return f"Top Author: {top_author.full_name} with {top_author.num_of_articles} published articles."


def get_top_reviewer():
    top_reviewer = Author.objects.annotate(
        count_of_published_reviews=Count('author_review')
    ).filter(count_of_published_reviews__gt=0).order_by('-count_of_published_reviews', 'email').first()

    if not top_reviewer or top_reviewer.count_of_published_reviews == 0:
        return ""

    return f"Top Reviewer: {top_reviewer.full_name} with {top_reviewer.count_of_published_reviews} published reviews."


def get_latest_article():
    latest_article = Article.objects.annotate(
        num_reviews=Count('article_review'),
        sum_rating=Sum("article_review__rating")
    ).last()

    if not latest_article:
        return ""

    authors_names = ', '.join([author.full_name for author in latest_article.authors.all().order_by('full_name')])

    if latest_article.num_reviews == 0:
        average_rating = 0
    else:
        average_rating = latest_article.sum_rating / latest_article.num_reviews
    return f"The latest article is: {latest_article.title}. Authors: {authors_names}. Reviewed: {latest_article.num_reviews} times. Average Rating: {average_rating:.2f}."


def get_top_rated_article():
    top_rated_article = Article.objects.annotate(
        num_reviews=Count('article_review'),
        avg_rating=Avg('article_review__rating')
    ).order_by('-avg_rating', 'title').first()

    if not Review.objects.all():
        return ""

    return f"The top-rated article is: {top_rated_article.title}, with an average rating of {top_rated_article.avg_rating:.2f}, reviewed {top_rated_article.num_reviews} times."


def ban_author(email=None):
    if email is None:
        return "No authors banned."

    author = Author.objects.filter(email__exact=email).first()

    if author is None:
        return "No authors banned."

    num_reviews_deleted = 0

    if not author.is_banned:
        num_reviews_deleted = author.author_review.count()
        author.author_review.all().delete()
        author.is_banned = True
        author.save()

    if num_reviews_deleted == 0 and email:
        return "No authors banned."

    return f"Author: {author.full_name} is banned! {num_reviews_deleted} reviews deleted."
