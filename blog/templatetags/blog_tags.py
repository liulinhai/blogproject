from django import template
from ..models import Post,Category,ViewNum,Tag
from django.db.models.aggregates import Count
from django.contrib.contenttypes.models import ContentType
from django_comments.models import Comment
from django.conf import settings
register = template.Library()

@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all()[:num]

@register.simple_tag
def archives():
    return Post.objects.dates('created_time','month',order='DESC')

@register.simple_tag
def get_categories():
    #return Category.objects.all()
    return Category.objects.annotate(num_posts=Count('post'))

@register.simple_tag
def get_view_num(post_id):
    obj_type = ContentType.objects.get_for_model(Post)
    v = ViewNum.objects.get_or_create(content_type=obj_type, object_id=post_id)
    return v[0].view_nums #一个post_id只生成一个ViewNums，取第一个即可。

@register.simple_tag
def get_comment_num(post_id):
    site_id = getattr(settings, "SITE_ID", None)
    ctype =ContentType.objects.get_for_model(Post)
    return len(Comment.objects.filter(
            content_type=ctype,
            object_pk=post_id,
            site__pk=site_id,
        ))

@register.simple_tag
def get_view_n(post):
    return sum(map(lambda x:x.view_nums,post.view_num.all()))

@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

#.filter(num_posts__gt=0) 大于0.