
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseRedirect
from .models import Post,Follow
from blogs.forms import PostForm
from django.contrib.auth import login  # for logging in the user
from django.contrib import messages
from django.shortcuts import render

def home(request):
    return render(request, 'blogs/home.html')

from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('login')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blogs/register.html', {'form': form})


from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def follow_toggle(request, user_id):
    target_user = get_object_or_404(User, id=user_id)

    if request.user == target_user:
        messages.error(request, "You cannot follow yourself.")
        return redirect('post_list')

    follow_obj, created = Follow.objects.get_or_create(
        follower=request.user,
        author=target_user
    )
    if not created:
        follow_obj.delete()
        messages.info(request, f"You unfollowed {target_user.username}.")
    else:
        messages.success(request, f"You are now following {target_user.username}.")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('post_list')))





def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blogs/post_list.html', {'posts': posts})


# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     user_follows_author = False

#     if request.user.is_authenticated:
#         user_follows_author =Follow.objects.filter(follower=request.user, author=post.author).exists()

#     context = {
#         'post': post,
#         'user_follows_author': user_follows_author,
#     }
#     return render(request, 'blogs/post_detail.html', context)
from django.contrib.auth.models import User
@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    followed_authors = request.user.follows.values_list('author_id', flat=True)
    return render(request, 'blogs/post_detail.html', {
        'post': post,
        'followed_authors': followed_authors,
    })



def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blogs/create_post.html', {'form': form})



@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blogs/create_post.html', {'form': form, 'edit': True})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')

    return render(request, 'blogs/post_confirm_delete.html', {'post': post})




