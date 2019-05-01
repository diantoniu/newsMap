from django.db import models

class News(models.Model):
    """
    Stores information about news
    """
    # date = models.DateTimeField(auto_now_add=False, blank=False)
    header = models.CharField(max_length=10000)
    news = models.CharField(max_length=10000)
