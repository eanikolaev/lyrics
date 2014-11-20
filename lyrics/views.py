from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from lyrics.models import Song
from search import search
import time
OK = 1
ERROR = 0


def round_time(seconds):
    return "%.2f" % seconds


def index(request):
    params_dict = {
    }

    return render(request, 'index.html', params_dict)


def song_list(request):    
    start_time = time.time()
    query = request.GET.get('query','')
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

    paginator = Paginator(song_list, 10)
    page = request.GET.get('page', None)
    if page:
        try:
            page_obj = paginator.page(page)
        except (PageNotAnInteger, EmptyPage) as e:
            page_obj = paginator.page(1)
    else:
        page_obj = paginator.page(1)


    params_dict = {
        'page_obj': page_obj,
        'results_count': count,
        'elapsed_time': round_time(time.time() - start_time)
    }

    return render(request, 'song_list.html', params_dict)


def error(request, msg):
    params_dict = {
        'message': msg
    }

    return render(request, 'error.html', params_dict)

