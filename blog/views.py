from django.db.models import F
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blog.forms import BlogPostForm
from blog.models import BlogPost


class BlogPostListView(ListView):
    """Список статей: только опубликованные."""

    model = BlogPost
    template_name = "blog/blogpost_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class BlogPostDetailView(DetailView):
    """Одна статья. При каждом открытии счётчик просмотров увеличивается на 1."""

    model = BlogPost
    template_name = "blog/blogpost_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        # F() увеличивает значение прямо в базе, без гонки при одновременных запросах
        BlogPost.objects.filter(pk=post.pk).update(views_count=F("views_count") + 1)
        post.refresh_from_db(fields=["views_count"])
        return post


class BlogPostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/blogpost_form.html"

    def get_success_url(self):
        return reverse("blog:post_detail", args=[self.object.pk])


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/blogpost_form.html"

    def get_success_url(self):
        # После редактирования — на страницу этой же статьи
        return reverse("blog:post_detail", args=[self.object.pk])


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = "blog/blogpost_confirm_delete.html"
    context_object_name = "post"
    success_url = reverse_lazy("blog:post_list")
