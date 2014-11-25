from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from lyrics.models import Song
from search import search
import time
OK = 1
ERROR = 0

def transform_query(query):
    if query and not ('and' in query.lower()) and not ('or' in query.lower()):
        return query.replace(' ', ' AND ')

    return query


def round_time(seconds):
    return "%.2f" % seconds


def index(request):
    params_dict = {
    }

    return render(request, 'index.html', params_dict)


def song_detail(request, song_id):    
    song = get_object_or_404(Song.objects.all(), id=song_id)
    params_dict = {
        'song': song
    }
    return render(request, 'song_detail.html', params_dict)


def song_list(request):    
    start_time = time.time()
    query = request.GET.get('query','')
    query = transform_query(query)
    if query:
        status, res = search(query.encode('utf-8'))
        if status == OK:
            song_list = Song.objects.filter(id__in=res)            
            count = song_list.count()
        else:
            return error(request, res)
    else:
        song_list = []
        count = 0


    params_dict = {
        'song_list': song_list,
        'results_count': count,
        'elapsed_time': round_time(time.time() - start_time)
    }

    return render(request, 'song_list.html', params_dict)


def error(request, msg):
    params_dict = {
        'message': msg
    }

    return render(request, 'error.html', params_dict)

