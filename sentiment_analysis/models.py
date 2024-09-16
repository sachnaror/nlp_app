from django.db import models


class Article(models.Model):
    url = models.URLField()
    sentiment_score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url
