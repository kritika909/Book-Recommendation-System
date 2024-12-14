from django.db import models
from django.contrib.auth.models import User
from textblob import TextBlob

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=225)
    immage = models.ImageField(upload_to='bookimg/', null=True)
    author = models.CharField(max_length=225)
    genre = models.CharField(max_length=50)
    description = models.TextField()
    publication_date = models.DateField()

    def __str__(self):
        return self.title
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True)
    text = models.TextField()
    sentiment = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.sentiment:
            analysis = TextBlob(self.text)
            self.sentiment = analysis.sentiment.polarity
        super().save(*args, **kwargs)

class ReadingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # read = models.BooleanField()

    class Meta:
        unique_together = ('user', 'book')
