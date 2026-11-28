from calendar import Calendar

from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.formats import date_format

from Dblog.models import Post
from Dstore.models import Category, Product

GAMES = {
    'pubg-mobile': ('PUBG Mobile', 'یوسی، اسکین و پاس', 'pubg', ('pubg',)),
    'call-of-duty-mobile': ('Call of Duty: Mobile', 'سی‌پی، اسکین و پاس', 'cod', ('codm', 'call-of-duty')),
    'free-fire': ('Free Fire', 'دایموند، اسکین و پاس', 'fire', ('free-fire-mobile',)),
    'clash-royale': ('Clash Royale', 'جم، پاس رویال و آیتم‌های ویژه', 'clash', ('clash-royale-mobile',)),
}


CURRENCY_LABELS = ('یوسی پابجی · UC', 'سی\u200cپی کالاف دیوتی · CP', 'الماس فری فایر · Diamond', 'جم کلش رویال · Gems')


def game_entries():
    return [
        {'slug': slug, 'name': name, 'services': services, 'style': style}
        for slug, (name, services, style, aliases) in GAMES.items()
    ]


def current_month_context():
    today = timezone.localdate()
    month_weeks = [
        [day or '' for day in week]
        for week in Calendar(firstweekday=5).monthdayscalendar(today.year, today.month)
    ]
    return {
        'current_month': date_format(today, 'F Y'),
        'month_weeks': month_weeks,
        'today_number': today.day,
    }


def home_view(request):
    games = game_entries()
    currency_labels = CURRENCY_LABELS
    games_by_category = {
        category_slug: slug
        for slug, (_, _, _, aliases) in GAMES.items()
        for category_slug in (slug, *aliases)
    }
    products = Product.objects.filter(
        is_active=True, product_type='currency', category__slug__in=games_by_category,
    ).select_related('category')
    featured = {}
    for product in products:
        featured.setdefault(games_by_category[product.category.slug], product)
        if len(featured) == len(games):
            break

    query = request.GET.get('q', '').strip()[:100]
    currencies = []
    for game, label in zip(games, currency_labels, strict=True):
        product = featured.get(game['slug'])
        search_text = f"{label} {game['name']} {game['services']} {product.title if product else ''}"
        if query.casefold() not in search_text.casefold():
            continue
        url = reverse('Dstore:category_detail', args=[product.category.slug]) if product else reverse(
            'Dpages:game_detail', args=[game['slug']],
        )
        currencies.append({'label': label, 'style': game['style'], 'product': product, 'url': url})

    return render(request, 'Dpages/home.html', {
        'games': games,
        'soundtrack': 'home',
        'currencies': currencies,
        'currency_query': query,
        'offer': Product.objects.filter(is_active=True, product_type='special_offer').select_related('category').first(),
        'posts': Post.objects.filter(is_published=True)[:3],
        **current_month_context(),
    })


def game_calendar_view(request):
    return render(request, 'Dpages/game_calendar.html', {'games': game_entries()})


def game_detail_view(request, game_slug):
    game = next((game for game in game_entries() if game['slug'] == game_slug), None)
    if game is None:
        raise Http404

    aliases = GAMES[game_slug][3]
    categories = Category.objects.filter(slug__in=(game_slug, *aliases)).in_bulk(field_name='slug')
    category = next((categories[slug] for slug in (game_slug, *aliases) if slug in categories), None)
    products = Product.objects.filter(
        is_active=True, category__in=categories.values(),
    ).select_related('category')[:12]
    article_slugs = (game_slug, *aliases)
    if game_slug == 'call-of-duty-mobile':
        article_slugs += ('کالاف', 'کالاف-دیوتی', 'کالاف-دیوتی-موبایل')
    posts = Post.objects.filter(is_published=True, category__slug__in=article_slugs)[:6]

    return render(request, 'Dpages/game_detail.html', {
        'game': game,
        'category': category,
        'products': products,
        'posts': posts,
        **current_month_context(),
        'soundtrack': game['style'],
    })
