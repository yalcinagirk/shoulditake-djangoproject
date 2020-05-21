from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from app import models
from app.forms import ProductForm, CategorySorguForm, CommentForm
from app.models import Product, FavoritedProduct
from django.http import HttpResponseBadRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

def deneme(request):
    return render(request, 'deneme.html')

class HomeView(TemplateView):
    template_name = "app/home/home.html"


class ProfileView(TemplateView):
    template_name = "app/profile/user_profile_base.html"


class ContactView(TemplateView):
    template_name = "app/profile/profile_contact.html"


class ReviewsView(TemplateView):
    template_name = "app/profile/profile_reviews.html"


def ArticleList(request):
    articles = models.Product.objects.all()
    form = CategorySorguForm(data=request.GET or None)
    page = request.GET.get('page', 1)
    if form.is_valid():
        taslak_yayin = form.cleaned_data.get('taslak_yayin')
        search = form.cleaned_data.get('search', None)
        if search:
            articles = articles.filter(Q(icerik__icontains=search) | Q(name__icontains=search))
    paginator = Paginator(articles, 3)
    try:
        articles = paginator.page(page)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        articles = paginator.page(1)

    context = {'articles': articles, 'form': form}
    return render(request, 'app/articles/article_list.html', context)


def ArticleDetails(request, slug):
    form = CommentForm()
    article = models.Product.objects.filter(slug=slug)
    if article:
        context = {'article': article, 'form': form}
        return render(request, 'app/articles/article_details.html', context)
    return render(request, '404.html')


@login_required
def ArticleCreate(request):
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(data=request.POST, files=request.FILES or None)
        if form.is_valid():
            product = form.save(commit=False)
            product.user =request.user
            product.save()

            messages.success(request, '<strong>%s</strong> başlıklı article oluşturuldu.' % (product.name),
                             extra_tags='success')
            return HttpResponseRedirect(product.get_absolute_url())
    return render(request, 'app/articles/article_create.html', context={'form': form})


@login_required
def ArticleUpdate(request, slug):
    product = get_object_or_404(Product, slug=slug)
    form = ProductForm(instance=product, data=request.POST or None, files=request.FILES or None)
    if request.user != product.user:
        return HttpResponseForbidden()

    if form.is_valid():
        product.update()
        return HttpResponseRedirect(reverse('details', kwargs={'slug': slug}))
    context = {'form': form, 'product': product}
    return render(request, 'app/articles/article_update.html', context=context)


@login_required
def ArticleDelete(request, slug):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('user_login'))
    product = get_object_or_404(Product, slug=slug)
    if request.user != product.user:
        return HttpResponseForbidden()
    product.delete()
    messages.success(request, '<strong>%s</strong> başlıklı makale silindi.' % (product.name), extra_tags='danger')
    return HttpResponseRedirect(reverse('articles'))


@login_required
def add_comment(request, slug):
    #if request.user.is_anonymous:
    #    return HttpResponseRedirect(reverse('user_login'))
    if request.method == 'GET':
        return HttpResponseBadRequest()
    product = get_object_or_404(Product, slug=slug)
    form = CommentForm(data=request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.product = product
        new_comment.user = request.user
        new_comment.save()
        messages.success(request, 'Tebrikler yorumunuz oluşturuldu.')
        return HttpResponseRedirect(product.get_absolute_url())

@login_required
def add_or_remove_favorite(request, slug):
    url = request.GET.get('next', None)
    product = get_object_or_404(Product, slug=slug)
    favori_product = FavoritedProduct.objects.filter(product=product, user=request.user)

    if favori_product.exists():
        favori_product.delete()
    else:
        FavoritedProduct.objects.create(product=product, user=request.user)
    if not url:
        url = reverse('articles')
    return HttpResponseRedirect(url)



