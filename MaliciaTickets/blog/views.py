from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


from django.contrib.auth.models import User


def noticia(request,pk):
    #SELECT * FROM POST WHERE ID=PK
    post = get_object_or_404(Post,pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def noticias(request):
    # SELECT * FROM POST
    posts = Post.objects.all()
    return render(request, 'blog/post_list_ext.html', {'posts': posts})

@login_required
def nueva_noticia(request):
    form = PostForm()
    return render(request,'blog/post_edit.html',{'form':form})


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
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})