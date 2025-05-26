from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import CommentForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q

def home(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'posts': posts, 'query': query})

def product_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()  # Lấy tất cả bình luận của bài viết
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('product_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'product_detail.html', {'post': post, 'comments': comments, 'form': form})

def register(request):
    if request.method == 'POST':
        # Tạo form với dữ liệu từ request
        form = UserCreationForm(request.POST)
        # Kiểm tra tính hợp lệ của form
        if form.is_valid(): 
            user = form.save()  # Lưu thông tin người dùng vào cơ sở dữ liệu
            login(request, user)
            # Thêm thông báo thành công
            messages.success(request, 'Đăng ký thành công! Chào mừng bạn đến với trang webhfgfghfhg.')
            return redirect('home')     # Chuyển hướng người dùng về trang chủ
    else:
        form = UserCreationForm()
    # Render template `register.html` với form
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)  # Tạo form với dữ liệu từ request
        if form.is_valid():  # Kiểm tra tính hợp lệ của form
            user = form.get_user()  # Lấy thông tin người dùng từ form
            login(request, user) 
            messages.success(request, 'Đăng nhập thành công! Chào mừng bạn quay lại.')  # Thêm thông báo thành công
            return redirect('home')  # Chuyển hướng người dùng về trang chủ
    else: 
        form = AuthenticationForm()  # Tạo một form trống để hiển thị
    return render(request, 'login.html', {'form': form})  # Render template `login.html` với form

def logout_view(request):
    logout(request)
    return redirect('home')  # Chuyển hướng về trang chủ sau khi đăng xuất

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.likes += 1
    post.save()
    if request.is_ajax():  # Kiểm tra nếu là yêu cầu AJAX
        return JsonResponse({'likes': post.likes})  # Trả về số lượng like
    return redirect('product_detail', post_id=post.id)

