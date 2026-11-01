from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, TemplateView

from catalog.forms import ContactForm
from catalog.models import Product


class HomeView(ListView):
    """Главная страница: список всех товаров."""

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.all()


class ProductDetailView(DetailView):
    """Страница одного товара. Если товара с таким pk нет, вернётся 404."""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ContactsView(TemplateView):
    """Страница контактов с формой обратной связи."""

    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("form", ContactForm())
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            messages.success(
                request, f"Спасибо, {contact.name}! Ваше сообщение отправлено."
            )
            # Перенаправление защищает от повторной отправки при обновлении страницы
            return redirect("catalog:contacts")
        # Форма с ошибками показывается снова
        return self.render_to_response(self.get_context_data(form=form))
