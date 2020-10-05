from django.shortcuts import render, get_object_or_404
from django.contrib.postgres.search import SearchVector
from django.db.models import Count
from .models import Post, Comment
from .filters import Filter
from .forms import CommentForm, FindForm, SearchForm
from taggit.models import Tag


def post_search(request):
    form = FindForm()
    tag = request.GET.get('tags')
    gs = []
    if tag:
        filter = {}
        filter['tags'] = tag
        gs = Post.objects.filter(**filter)
    print(gs)
    return render(request, 'blog/search.html', {'gs': gs, 'form': form})


def post_list(request, tag_slug=None):
    posts = Post.objects.all()
    tags = Tag.objects.all()
    tag = None
    myFilter = Filter(request.GET, queryset=posts)
    posts = myFilter.qs
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    return render(request, 'blog/home.html', {'posts': posts,
                                              'tag': tag,
                                              'myFilter': myFilter})


def post_detail(request, pk):
    post = get_object_or_404(Post, id = pk)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in = post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'blog/post_detail.html', {'post': post,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form,
                                                     'similar_posts': similar_posts})
