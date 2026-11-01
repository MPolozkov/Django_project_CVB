from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Удаляет все категории и продукты и загружает тестовые данные из фикстур"

    @transaction.atomic
    def handle(self, *args, **options):
        # Сначала продукты (они ссылаются на категории), затем категории
        deleted_products, _ = Product.objects.all().delete()
        deleted_categories, _ = Category.objects.all().delete()
        self.stdout.write(
            f"Удалено продуктов: {deleted_products}, категорий: {deleted_categories}"
        )

        # Категории загружаются первыми, чтобы связи ForeignKey у продуктов выстроились
        call_command("loaddata", "category.json")
        call_command("loaddata", "product.json")

        self.stdout.write(
            self.style.SUCCESS(
                f"Загружено категорий: {Category.objects.count()}, "
                f"продуктов: {Product.objects.count()}"
            )
        )
