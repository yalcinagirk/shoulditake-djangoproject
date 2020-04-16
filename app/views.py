from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views.generic import TemplateView
from app import models
from app.forms import ProductForm, CategorySorguForm
from app.models import Product


class HomeView(TemplateView):
    template_name = "app/home/home.html"


class ProfileView(TemplateView):
    template_name = "app/profile/public_profile.html"


class ContactView(TemplateView):
    template_name = "app/profile/profile_contact.html"


class ReviewsView(TemplateView):
    template_name = "app/profile/profile_reviews.html"


def ArticleList(request):
    articles = models.Product.objects.all()
    form = CategorySorguForm(data = request.GET or None)
    context = {'articles':articles}
    return render(request, 'app/articles/article_list.html', context)


def ArticleDetails(request, slug):
    article = models.Product.objects.filter(slug=slug)
    if article:
        context = {'article': article}
        return render(request, 'app/articles/article_details.html', context)
    return render(request,'404.html')

def ArticleCreate(request):
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(data=request.POST, files=request.FILES or None)
        if form.is_valid():
            product = form.save()
            messages.success(request,'<strong>%s</strong> başlıklı article oluşturuldu.'% (product.name),extra_tags='success')
            return  HttpResponseRedirect(product.get_absolute_url())
    return render(request, 'app/articles/article_create.html', context={'form':form})
def ArticleUpdate(request, slug):
    product = get_object_or_404(Product, slug=slug)

    form = ProductForm(instance=product, data=request.POST or None, files=request.FILES or None)
    context = {'form':form, 'product':product}

    if form.is_valid():
        form.save()
        messages.success(request,'<strong>%s</strong> başlıklı article güncellendi.'% (product.name), extra_tags='info')
        return HttpResponseRedirect(reverse('details',kwargs={'slug':slug}))
    return render(request,'app/articles/article_update.html',context=context)
def ArticleDelete(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product.delete()
    messages.success(request, '<strong>%s</strong> başlıklı makale silindi.' % (product.name), extra_tags='danger')
    return HttpResponseRedirect(reverse('articles'))



