from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from blog.models import Author, Category


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render_to_response('blog/category_detail.html',
        {'object_list': category.live_entry_set(), 'category': category},
        context_instance=RequestContext(request))


def author_detail(request, id):
    author = get_object_or_404(Author, pk=id)
    return render_to_response('blog/author_detail.html',
        {'object_list': author.live_entry_set(), 'author': author},
        context_instance=RequestContext(request))
