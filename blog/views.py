from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.contrib import messages
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from . models import Post, Category
from django.db.models import Count
from django.db.models import F
from django.urls import reverse
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.


# Home
def home(request):
    popular_posts = Post.objects.order_by('-views')[:6]

    context = {
        'popular_posts': popular_posts
    }

    return render(request, 'blog/base.html', context)


# Blog List
def blog_list(request):
    post_list = Post.objects.all()
    categories = Category.objects.all()

    paginator = Paginator(post_list, 9)  # Show 6 posts per page

    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'blog/blog_list.html', {'posts': posts, 'categories': categories})
    posts = Post.objects.all()
    categories = Category.objects.all()

    return render(request, 'blog/blog_list.html', {'posts': posts, 'categories': categories})


# Blog Details
def blog_detail(request, category_slug, post_slug):
    category = get_object_or_404(Category, slug=category_slug)
    post = get_object_or_404(Post, slug=post_slug, category=category)
    related_posts = Post.objects.filter(
        category=category).exclude(slug=post_slug)[:4]
    recent_posts = Post.objects.order_by('-date_posted')[:10]
    context = {
        'post': post,
        'related_posts': related_posts,
        'recent_posts': recent_posts
    }
    return render(request, 'blog/blog_detail.html', context)


# Dashboard
@login_required(login_url='/login')
def dashboard(request):
    if request.user.is_staff:
        data = Post.objects.all()
    else:
        data = Post.objects.filter(author=request.user)
    context = {'data': data}
    return render(request, 'blog/dashboard.html', context)


# Edit Posts
@login_required(login_url='/login')
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            # Check if logged-in user is not an admin before updating author
            if not request.user.is_superuser:
                post.author = request.user
            post.save()
            messages.success(
                request, 'Your post has been updated Succesfully!')
            return redirect('/dashboard')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form': form})


@login_required
def delete_post(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        post.delete()
        messages.success(request, 'Post deleted successfully.')
        return redirect('/dashboard')


# Search Posts
def search(request):
    query = request.GET['query']
    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query))
    context = {'posts': posts}
    return render(request, 'blog/search.html', context)


# Category List
def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category)
    context = {'category': category, 'posts': posts}
    return render(request, 'blog/category.html', context)


# contact
def contact(request):
    return render(request, 'blog/contact.html')


# About
def about(request):
    return render(request, 'blog/about.html')


# User Logout
@login_required(login_url='/login')
def user_logout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out!')
    return HttpResponseRedirect('/login')


# User Login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                user_name = form.cleaned_data['username']
                user_password = form.cleaned_data['password']
                user = authenticate(username=user_name, password=user_password)
                if user is not None:
                    login(request, user)
                    messages.success(
                        request, f'Welcome back <strong> {user.username}</strong>')
                    # update session activity timestamp
                    # request.session['last_activity'] = datetime.now()
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()

        # # check if session has expired
        # last_activity = request.session.get('last_activity')
        # if last_activity is not None:
        #     # calculate time elapsed since last activity
        #     now = datetime.now()
        #     time_elapsed = now - last_activity
        #     if time_elapsed > timedelta(seconds=request.session.get_expiry_age()):
        #         # session has expired, logout user
        #         logout(request)
        #         messages.warning(
        #             request, 'Session has expired. Please login again.')

        return render(request, 'blog/accounts/login.html', {'form': form})
    else:
        return HttpResponseRedirect('/dashboard/')


# User Signup Form
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(
                request, 'Your account has been registered!!  Now you can login')
            form.save()
            form = SignUpForm()
            return HttpResponseRedirect('/login')
    else:
        form = SignUpForm()
    return render(request, 'blog/accounts/signup.html', {'form': form})


# Add Post
@login_required(login_url='/login')
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                messages.success(
                    request, 'Your Post has been Published successfully.')
                return HttpResponseRedirect('/dashboard')
        else:
            form = PostForm()
        categories = Category.objects.all()
        return render(request, 'blog/add_post.html', {'form': form, 'categories': categories})
    else:
        return HttpResponseRedirect('/login')
