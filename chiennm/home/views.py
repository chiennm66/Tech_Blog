from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import CommentForm



def home(request):
    posts = Post.objects.all().order_by('-created_at')  # Lấy bài viết mới nhất
    return render(request, 'index.html', {'posts': posts})



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

