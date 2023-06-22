from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def noticia(request,pk):
    #SELECT * FROM POST WHERE ID=PK
    post = get_object_or_404(Post,pk=pk)
    return render(request, 'blog/noticia.html', {'post': post})

def noticias(request):
    # SELECT * FROM POST
    posts = Post.objects.all()
    return render(request, 'blog/noticias.html', {'posts': posts})

@login_required
def nueva_noticia(request):
    form = PostForm()
    return render(request,'blog/editar_noticia.html',{'form':form})


@login_required
def editar_noticia(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('noticia', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/editar_noticia.html', {'form': form})