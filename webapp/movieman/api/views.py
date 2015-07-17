from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from common.models import Movie


def yearHist(request):
    yearHist = Movie.objects.values('year').annotate(count=Count('year'))
    return JsonResponse(dict(data=list(yearHist)))
def query(request):
    title = request.GET.get('title','')
    #movies = Movie.objects.filter(title__contains=title).values(*Movie.fields)
    movies =Movie.objects.queryByTitle(title)
    return JsonResponse(dict(data=list(movies)))
def detail(request,id):
    print id
    movies = Movie.objects.filter(id =id).values(*Movie.fields)
    return JsonResponse(dict(data=list(movies)))
