from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from .models import Posts
from .forms import PostCreateForm, PostUpdateForm

# 게시글 등록
def posts_create(request):
    form = PostCreateForm()
    
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, '게시글이 등록되었습니다.')
            return redirect("posts:read", post_id=post.id)
        else:
            messages.error(request, '게시글 등록에 실패했습니다.')
    
    return render(request, 'posts/create.html', {'form': form})

# 게시글 보기
def posts_read(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    return render(request, 'posts/read.html', {'post': post})

# 게시글 수정
def posts_update(request, post_id):
    post = get_object_or_404(Posts, id=post_id)    
    form = PostUpdateForm(instance=post)
    
    if request.method == 'POST':
        form = PostUpdateForm(request.POST)
        
        if form.is_valid():
            if form.cleaned_data['password'] == post.password:
                post = form.save(commit=False)
                post.save()
                messages.success(request, '게시글이 수정되었습니다.')
                return redirect('posts:read', post_id=post.id)
            else:
                messages.error(request, '비밀번호가 일치하지 않습니다.')
        else:
            messages.error(request, '게시글 수정에 실패했습니다.')

    return render(request, 'posts/update.html', {'form': form})

# 게시글 삭제
def posts_delete(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    password = request.POST.get('password')
    
    if request.method == 'POST':
        if password == post.password:
            post.delete()
            messages.success(request, '게시글이 삭제되었습니다.')
            return redirect('posts:list')
        else:
            messages.error(request, '비밀번호가 일치하지 않습니다.')
            return redirect('posts:read', post_id=post.id)

# 게시글 목록
def posts_list(request):
    posts = Posts.objects.all().order_by('-created_at')
    return render(request, 'posts/list.html', {'posts': posts})