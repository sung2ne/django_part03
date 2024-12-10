from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib import messages

from .models import Posts
from .forms import PostCreateForm, PostUpdateForm

# 게시글 등록
def posts_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, '게시글이 등록되었습니다.')
            return redirect("posts:read", post_id=post.id)
        else:
            for field_name, error_messages in form.errors.items():
                messages.error(request, f"{form.fields[field_name].label}: {error_messages[0]}")

    form = PostCreateForm()        
    return render(request, 'board/create.html', {'form': form})

# 게시글 보기
def posts_read(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    return render(request, 'posts/read.html', {'post': post})

# 게시글 수정
def posts_update(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    
    if request.method == 'POST':
        form = PostUpdateForm(request.POST, instance=post)
        
        if form.is_valid():
            if form.cleaned_data['passwd'] == post.passwd:
                post = form.save(commit=False)
                post.save()
                messages.success(request, '게시글이 수정되었습니다.')
                return redirect('posts:read', post_id=post.id)
            else:
                messages.error(request, '비밀번호가 일치하지 않습니다.')
        else:
            for field_name, error_messages in form.errors.items():
                messages.error(request, f"{form.fields[field_name].label}: {error_messages[0]}")
    else:
        form = PostUpdateForm(instance=post)
        
    return render(request, 'posts/update.html', {'form': form})

# 게시글 삭제
def posts_delete(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    
    if request.method == 'POST':
        if request.POST['passwd'] == post.passwd:
            post.delete()
            messages.success(request, '게시글이 삭제되었습니다.')
            return redirect('posts:list')
        else:
            messages.error(request, '비밀번호가 일치하지 않습니다.')
            return redirect('posts:read', post_id=post.id)

# 게시글 목록
def posts_list(request):
    posts = Posts.objects.all().order_by('-id')
    return render(request, 'posts/list.html', {'posts': posts})