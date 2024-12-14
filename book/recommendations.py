from django.db.models import Q
from .models import Book, ReadingHistory, Review
from django.contrib.auth.models import User

def get_content_based_rec(user):
    liked_books = Review.objects.filter(user=user, rating__gte=4).values('book')
    genres = Book.objects.filter(id__in=liked_books).values_list('genre', flat=True)
    authors = Book.objects.filter(id__in=liked_books).values_list('author', flat=True)

    recs = Book.objects.filter(
        Q(genre__in=genres) | Q(author__in=authors)
    ).exclude(readinghistory__user=user).distinct()
    return recs

def get_collaborative_rec(user):
    user_books = ReadingHistory.objects.filter(user=user).values_list('book', flat=True)
    similar_users = User.objects.filter(readinghistory__book__in=user_books).exclude(id=user.id).distinct()

    similar_books = Review.objects.filter(user__in=similar_users, rating__gte=4).values_list('book', flat=True)

    recs = Book.objects.filter(id__in=similar_books).exclude(readinghistory__user=user).distinct()
    return recs