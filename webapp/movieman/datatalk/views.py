from django.db.models import Count
from django.http import HttpResponse,Http404, JsonResponse
from django.shortcuts import render
from django.template import RequestContext,loader
# Create your views here.
from common.models import Movie


def index(request):
    movies = Movie.objects.values('title','siteScore')[0:1]
    # template = loader.get_template('index.html')
    # context = RequestContext(request,{
    #     'movies' :movies
    # })
    # return HttpResponse(template.render(context))

    context={'movies':movies}
    #return render(request,'index.html',context)
    return JsonResponse(dict(data=list(movies)))

