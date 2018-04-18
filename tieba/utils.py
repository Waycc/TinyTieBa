from django.shortcuts import redirect
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator

def is_login(func):
    def wrap(request,*args, **kwargs):
        if request.user.__str__() != 'AnonymousUser' and request.user:
            return redirect('/tieba/index/')
        else:
            return func(request,*args,**kwargs)
    return wrap


def query_set(obj_list, page, per_page_num=10):
    """返回分页后的对象"""
    paginator = Paginator(obj_list, per_page_num)
    try:
        query_sets = paginator.page(page)
    except PageNotAnInteger:
        query_sets = paginator.page(1)
    except EmptyPage:
        query_sets = paginator.page(paginator.num_pages)
    return query_sets