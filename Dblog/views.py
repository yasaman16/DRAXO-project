from django.shortcuts import render, get_object_or_404
from .models import Post

def post_list_view(request):
    posts = Post.objects.filter(is_published=True)
    return render(request, 'Dblog/post_list.html', {'posts': posts})

def post_detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    return render(request, 'Dblog/post_detail.html', {'post': post})
