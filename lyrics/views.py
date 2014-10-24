from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from lyrics.models import Song


def index(request):
    params_dict = {
    }

    return render(request, 'index.html', params_dict)


def song_list(request):
    song_list = Song.objects.all()
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
        'results_count': song_list.count()
    }

    return render(request, 'song_list.html', params_dict)
 
