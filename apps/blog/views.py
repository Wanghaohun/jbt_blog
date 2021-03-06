from django.shortcuts import render
from apps.blog.models import Article, Category, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.conf import settings
from haystack.views import SearchView

categories = Category.objects.all()  # 获取全部的分类对象
tags = Tag.objects.all()  # 获取全部的标签对象
months = Article.objects.datetimes('pub_time', 'month', order='DESC')[:2]

# Create your views here.
def home(request):  # 主页
    posts = Article.objects.filter(status='p', pub_time__isnull=False)  # 获取全部(状态为已发布，发布时间不为空)Article对象
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
    page = request.GET.get('page')  # 获取URL中page参数的值
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {'post_list': post_list, 'category_list': categories, 'months': months})


def detail(request, id):
    try:
        post = Article.objects.get(id=str(id))
        post.viewed()  # 更新浏览次数
        category = categories.get(id=post.category_id)
        tags = post.tags.all()
        next_post = post.next_article()  # 上一篇文章对象
        prev_post = post.prev_article()  # 下一篇文章对象
    except Article.DoesNotExist:
        raise Http404
    return render(
        request, 'post.html',
        {
            'post': post,
            'tags': tags,
            'category_list': categories,
            'category': category,
            'next_post': next_post,
            'prev_post': prev_post,
            'months': months
        }
    )


def search_category(request, categoryname):
    posts = Article.objects.filter(category__name=categoryname)
    category = categories.get(name=categoryname)
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
    try:
        page = request.GET.get('page')  # 获取URL中page参数的值
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'category.html',
                  {'post_list': post_list,
                   'category_list': categories,
                   'category': category,
                   'months': months
                  }
    )


def search_tag(request, tag):
    posts = Article.objects.filter(tags__name__contains=tag)
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
    try:
        page = request.GET.get('page')  # 获取URL中page参数的值
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'tag.html', {
        'post_list': post_list,
        'category_list': categories,
        'tag': tag,
        'months': months
        }
    )


def archives(request, year, month):
    posts = Article.objects.filter(pub_time__year=year, pub_time__month=month).order_by('-pub_time')
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
    try:
        page = request.GET.get('page')  # 获取URL中page参数的值
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'archive.html', {
        'post_list': post_list,
        'category_list': categories,
        'months': months,
        'year_month': year+'年'+month+'月'
        }
    )
class MySearchView(SearchView):
    template = 'search.html'
    def get_context(self):
        (paginator, page) = self.build_page()

        context = {
            'query': self.query,
            'form': self.form,
            'page': page,
            'paginator': paginator,
            'suggestion': None,
            'category_list': categories,
            'months': months
        }

        if hasattr(self.results, 'query') and self.results.query.backend.include_spelling:
            context['suggestion'] = self.form.get_suggestion()

        context.update(self.extra_context())

        return context