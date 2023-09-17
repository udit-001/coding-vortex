from .models import Category
from django.db.models import Count

def categories(request):
    all_categories = Category.objects.annotate(Count('posts'))

    not_empty_categories = all_categories.filter(posts__count__gt=0)

    return {
        'categories': not_empty_categories
    }