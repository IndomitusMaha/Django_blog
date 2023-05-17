from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # default is app_name/Model_ViewType.html (for example blog/post_list.html)
    context_object_name = 'posts' #Becouse we already referenced variable named posts home.html template (default is object_list)
    ordering = ['-date'] #coulmn crated by me for Post. -sign in '-date' because ORDER BY DESC


class PostDetailView(DetailView):
    model = Post #deafult template for DetailView name is app_name/Modelname_detail.html


class PostCreateView(LoginRequiredMixin, CreateView): #class version off @login_required
    model = Post #deafult template for CreateView name is app_name/Modelname_form.html
    fields = ['title', 'content'] #fileds we want file

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): #class version off @login_required
    # UserPassesTestMixin is to validate if your author of the post
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # func to check that post is yours
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post # defrault template is Modelname_confirm_delete.html
    success_url = '/'

    # func to check that post is yours
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
