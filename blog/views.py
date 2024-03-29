from django.http import Http404
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render , get_object_or_404, redirect
from .models import Post, Like, Comment
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.generic import ListView, CreateView
from django.core.paginator import Paginator
from .forms import CreateUserFrom, LoginForm, CommentForm
from django.contrib.auth.decorators import login_required


class SignUpViews(CreateView):
    form_class = CreateUserFrom
    success_url = reverse_lazy('blog:my_login')
    template_name = 'registration/signup.html'


def my_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('blog:home')
    else:
        form = LoginForm
    return render(request, 'registration/login.html', {'form':form})

    data = {
        'form': form,
    }
        

def home(request):
    return render(request, 'blog/home.html')


def user_logout(request):
    logout(request)
    return redirect("blog:home")

class PostListViews(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'blog/post/list.html'



# def post_list(request):
#     post_list = Post.published.all()
#     paginator = Paginator(post_list, 4)
#     page_number = request.GET.get('page', 1)
#     try:
#         posts = paginator.page(page_number)
#     except:
#         posts = paginator.page(1)

#     return render(request,
#                   'blog/post/list.html',
#                   {'posts': posts})


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=slug,
        publish__year=year,
        publish__month=month,
        publish__day=day
        )
    comments = Comment.objects.filter(post=post)
    like = Like.objects.filter(post=post)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('blog:post_detail', year=year, month=month, day=day, slug=post.slug)

    else:
        comment_form = CommentForm()


    data = {'post': post,
             'like': like,
             'comments': comments,
             'comment_form': comment_form
            }
    return render(request, 'blog/post/detail.html', data) 

def like_post(request, post_id):
    post = get_object_or_404(post, id=post_id)

    liked, crated = Like.objects.get_or_create(post=post, user=request.user)

    if not crated:
        liked.dalate()

    likes_count = post.li8kes.count()

    return JsonResponse({'likes_count': likes_count})



@login_required
def dashboard(request, id):
    if request.user.id == id:
        user = get_object_or_404(User, id=id)

        data = {
        'user': user
        }
        return render(request, 'dashboard.html', data)
    else:
        return redirect("blog:home")
























