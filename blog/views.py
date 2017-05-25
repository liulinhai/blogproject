from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post,Category,ViewNum
from django.contrib.auth.models import User
from .paginator import getPages
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count

#import markdown
# Create your views here.


def index(request):

    #post_list = Post.objects.all()

    post_list=Post.objects.annotate(Count('view_num'))#只是取到对象，不能取到对象对应的字段
    data = {}
    pages, post_list = getPages(request,post_list)

    data['post_list'] = post_list
    data['pages'] = pages

    if 'xyz' in request.META['HTTP_HOST']:
        return render(request, 'blog/index.html', data )
    else:
        return render(request, 'blog/index2.html', data)

def detail(request,pk):
    post = get_object_or_404(Post,pk=pk)

    strs = 'post_%s_readed'% pk

    obj_type = ContentType.objects.get_for_model(Post)
    v = ViewNum.objects.get_or_create(content_type=obj_type,object_id=post.id)
    if strs not in request.COOKIES:
        v[0].view_nums+=1
        v[0].save()


    #previous blog
    pre_post=Post.objects.filter(id__lt=pk).order_by('-id')
    if pre_post.exists():
        pre_post=pre_post[0]
    else:
        pre_post={}

    next_post=Post.objects.filter(id__gt=pk)
    if next_post.exists():
        next_post=next_post[0]
    else:
        next_post={}

    data = {}
    """
    if request.user.is_authenticated:
        data['change']=True
    else:
        data['change']=False
    """
    #data['user']=request.user
    data['post']=post
    data['pre_post']=pre_post
    data['next_post']=next_post
    #data['view_num']=v[0]

    if 'xyz' in request.META['HTTP_HOST'] :

        response = render(request,'blog/detail.html',data)
    else:
        response = render(request, 'blog/detail2.html', data)

    response.set_cookie( strs,True)
    return response

def archives(request,year,month):
    post_list = Post.objects.filter(created_time__year=year,created_time__month=month)
    data = {}
    pages, post_list = getPages(request,post_list)

    data['post_list'] = post_list
    data['pages'] = pages

    if 'xyz' in request.META['HTTP_HOST']:
        return render(request, 'blog/index.html', data )
    else:
        return render(request, 'blog/index2.html', data)
    #return render(request, 'blog/index.html', data )

def category(request,pk):
    cate = get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(category=cate)
    data = {}
    pages, post_list = getPages(request,post_list)

    data['post_list'] = post_list
    data['pages'] = pages

    if 'xyz' in request.META['HTTP_HOST']:
        return render(request, 'blog/index.html', data )
    else:
        return render(request, 'blog/index2.html', data)
    #return render(request, 'blog/index.html', data )

def categoryn(request,pk):
    cate = get_object_or_404(Category,name=pk)
    post_list = Post.objects.filter(category=cate)
    data = {}
    pages, post_list = getPages(request,post_list)

    data['post_list'] = post_list
    data['pages'] = pages

    if 'xyz' in request.META['HTTP_HOST']:
        return render(request, 'blog/index.html', data )
    else:
        return render(request, 'blog/index2.html', data)
    #return render(request, 'blog/index.html', data )

def authors(request,pk):
    author = get_object_or_404(User,username=pk)
    post_list = Post.objects.filter(author=author)
    data = {}
    pages, post_list = getPages(request,post_list)

    data['post_list'] = post_list
    data['pages'] = pages

    if 'xyz' in request.META['HTTP_HOST']:
        return render(request, 'blog/index.html', data )
    else:
        return render(request, 'blog/index2.html', data)

def search(request):
    str=request.GET['search']
    post_list = Post.objects.filter(title__icontains=str)
    data = {}
    pages, post_list = getPages(request,post_list)

    data['post_list'] = post_list
    data['pages'] = pages

    return render(request, 'blog/index.html', data )

def test(request):
    values = request.META.items()
    #values.sort()
    html=[]
    for k,v in values:
        html.append('<tr><td>%s<td><td>%s<td></tr>' % (k,v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))


def contact(request):
    return render(request,'blog/contact.html')