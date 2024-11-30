from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Post, Category, Comment

# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published=True).order_by('-created_at')
    categories = Category.objects.all()
    
    # Filter by category if specified
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=category)
    
    paginator = Paginator(posts, 6)  # Show 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_slug,
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    comments = post.comments.filter(active=True)
    recent_posts = Post.objects.filter(
        published=True
    ).exclude(id=post.id).order_by('-created_at')[:3]
    
    context = {
        'post': post,
        'comments': comments,
        'recent_posts': recent_posts,
    }
    return render(request, 'blog/post_detail.html', context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(
        category=category,
        published=True
    ).order_by('-created_at')
    
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category_detail.html', context)

def add_comment(request, slug):
    if request.method == 'POST':
        post = get_object_or_404(Post, slug=slug)
        name = request.POST.get('name')
        email = request.POST.get('email')
        content = request.POST.get('content')
        
        try:
            Comment.objects.create(
                post=post,
                name=name,
                email=email,
                content=content
            )
            messages.success(request, "Your comment has been submitted and is awaiting moderation.")
        except Exception as e:
            messages.error(request, "There was an error submitting your comment. Please try again.")
    
    return redirect('blog:post-detail', slug=slug)

def search(request):
    query = request.GET.get('q', '')
    if query:
        posts = Post.objects.filter(
            published=True
        ).filter(
            title__icontains=query
        ) | Post.objects.filter(
            published=True
        ).filter(
            content__icontains=query
        )
    else:
        posts = Post.objects.filter(published=True)
    
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'blog/post_list.html', context)
