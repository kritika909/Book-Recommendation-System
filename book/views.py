from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book, Review, ReadingHistory
from .recommendations import get_collaborative_rec, get_content_based_rec
# Create your views here.

@login_required
def book(request):
    books = Book.objects.all()
    return render(request, "book.html", {"books": books})

@login_required
def bookDetail(request, bookid):
    book = Book.objects.get(id=bookid)
    reviews = Review.objects.filter(book=book)
    data = {
        'bookDetails':book,
        'reviews':reviews
    }
    if request.method=='POST' and "read" in request.POST:
        ReadingHistory.objects.get_or_create(user=request.user, book=book)

    if request.method=='POST' and "review" in request.POST:
        review = request.POST['review']
        Review.objects.create(
            user=request.user,
            book=book,
            text=review,
        )
        
        return redirect('bookDetail', bookid=book.id)


    return render(request, "bookDetail.html", data)

@login_required
def recomm(request):
    user = request.user
    content_rec = get_content_based_rec(user)
    collab_rec = get_collaborative_rec(user)
    rec = (content_rec | collab_rec).distinct() 
    data = {
        'recs': rec
    }
    return render(request, "recomm.html", data)
