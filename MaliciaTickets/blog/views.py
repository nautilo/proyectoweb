from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required

def noticia(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/noticia.html', {'post': post})

def noticias(request):
    posts = Post.objects.all()
    return render(request, 'blog/noticias.html', {'posts': posts})

@login_required
def nueva_noticia(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.fecha_publicacion = timezone.now()
            post.save()
            return redirect('noticia', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/editar_noticia.html', {'form': form})
@login_required
def editar_noticia(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.save()  # Eliminar la línea 'post.published_date = timezone.now()'
            return redirect('noticia', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/editar_noticia.html', {'form': form})