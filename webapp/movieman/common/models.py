from __future__ import unicode_literals

from django.db import models

# Create your models here.
class MovieManager(models.Manager):
    pass
class Movie(models.Model):
    fields = ["id", "title", "year", "type", "imdbId", "imdbScore", "introduction", "runtime", "poster", "download", "site", "siteId", "siteStars", "siteVoteCount", "siteScore"]
    id = models.CharField(max_length=100,unique=True,primary_key=True)
    title = models.CharField(max_length=200,null=True)
    year = models.IntegerField(default=0)
    type = models.CharField(max_length=200,null=True)
    #genres =
    #areas =
    #languages =
    #pubTime =
    #alias =
    #screenwriters =
    #directors =
    #actors =
    imdbId = models.CharField(max_length=200,default=0)
    imdbScore = models.FloatField(default=0.0,null=True)
    introduction = models.TextField(null=True)
    runtime= models.IntegerField(default=0)
    poster  = models.CharField(max_length=200,null=True)
    download =models.CharField(max_length=400,null=True)
    site = models.CharField(max_length=20,null=True)
    siteId =models.CharField(max_length=100,null=True)
    siteScore =models.FloatField(default=0.0,null=True)
    siteStars =models.CharField(max_length=30)
    siteVoteCount =models.IntegerField(default=0)
    def __unicode__(self):
        return self.title
    def queryByTitle(self,title):
        return self.objects.filter(title__contains=title).values(*Movie.fields)

class Genres(models.Model):
    movie = models.ForeignKey(Movie)
    genreName = models.CharField(max_length=20)
class Areas(models.Model):
    movie = models.ForeignKey(Movie)
    area = models.CharField(max_length=100)
class Language(models.Model):
    movie = models.ForeignKey(Movie)
    language = models.CharField(max_length=100)
class PubTime(models.Model):
    movie = models.ForeignKey(Movie)
    pubTime = models.CharField(max_length=100)
class Alia(models.Model):
    movie = models.ForeignKey(Movie)
    Alia = models.CharField(max_length=200)
class Director(models.Model):
    movie = models.ForeignKey(Movie)
    director = models.CharField(max_length=100)