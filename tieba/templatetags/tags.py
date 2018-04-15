from django import template
import time
import datetime
from django.utils.safestring import mark_safe
from tieba import models

register = template.Library()

@register.simple_tag
def return_limit_content(content):
    """返回30个字符的字符串"""
    return mark_safe(content[0:30])


@register.simple_tag
def return_limit_name(name):
    if len(name) > 5:
        name = ''.join([name[0:4],'....'])
    else:
        name = name
    return name

@register.simple_tag
def return_format_time(date_time, full=None):
    """返回指定的时间格式"""
    current_time = datetime.datetime.now()
    a = date_time.strftime("%Y-%m-%d")
    if current_time.strftime("%Y-%m-%d") == a:
        date_time = date_time.strftime("%H:%M")
    elif full:
        date_time = date_time.strftime('%Y-%m-%d %H:%M')
    else:
        date_time = date_time.strftime('%m-%d')

    return date_time

floor = 1

@register.simple_tag
def return_floor():
    """返回评论楼层"""
    global floor
    floor += 1
    return floor

@register.simple_tag
def clean_floor():
    global floor
    floor = 1
    return mark_safe('<div></div>')

@register.simple_tag
def return_sub_comment_obj(comment_obj, article_obj):
    """返回主评论里的所有子评论"""
    comment_id = comment_obj.id
    sub_comment_obj_list = article_obj.comment_set.filter(to_comment_id=comment_id)
    return sub_comment_obj_list

@register.simple_tag
def return_to_whom_obj(sub_comment_obj):
    """返回子评论中给谁评论的对象"""
    to_whom_id = sub_comment_obj.to_whom
    if to_whom_id:
        to_whom_obj = models.UserProfile.objects.filter(id=int(to_whom_id)).first()
        return to_whom_obj

@register.simple_tag
def is_followed(request, tieba_obj):
    try:
        has_tieba_obj = request.user.followed_tieba.filter(name=tieba_obj.name)
    except AttributeError as e:
        return False
    return  has_tieba_obj

@register.simple_tag
def is_AnonymousUser(request):
    if request.user.__str__() != 'AnonymousUser' and request.user:
        return False
    else:
        return True

@register.simple_tag
def count_date(create_date):
    year, month, day = create_date.strftime('%Y-%m-%d').split('-')
    current_year, current_month, current_day = datetime.datetime.now().strftime('%Y-%m-%d').split('-')
    r_year = int(current_year)-int(year)
    r_month = int(current_month)-int(month)
    r_day = int(current_day)-int(day)
    if r_year == 0 and r_month == 0:
        result = '%s天'%r_day
    else:
        result = '%s.%s年'%(r_year,r_month)
    return result


def return_page_range(num_pages, current_page):
    '''分页用的'''
    if current_page < 5 :
        if num_pages<10:
            page_range = range(1,num_pages+1)
        else:
            page_range = range(1, 10)
    else:
        if current_page > num_pages-5:
            if num_pages-8 <= 0:
                page_range = range(1,num_pages+1)
            else:
                page_range = range(num_pages-8, num_pages+1)
        else:
            page_range = range(current_page-4, current_page+5)
    return page_range


@register.simple_tag
def return_page_ele(query_set, tieba_obj):
    ele = ''
    num_pages = query_set.paginator.num_pages    #总页数
    current_page = query_set.number   # 当前页
    page_range = return_page_range(num_pages,current_page)
    tieba = tieba_obj.name
    for page in page_range:
        if page == query_set.number:
            ele += '<span class="page-item current-page">%s</span>'%(page)
        else:
            ele += '<a class="page-item" href="?kw=%s&p=%s">%s</a>'%(tieba,page, page)
    return mark_safe(ele)

