from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest, JsonResponse
from following.models import Following
from django.template.loader import render_to_string
# Create your views here.
from django.contrib.auth.models import User


def kullanici_takip_et_cikar(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()

    data = {'html': ' ','is_valid': True, 'msg':'<b>Takip Ediliyor</b>'}
    follower_username = request.GET.get('follower_username', None)
    followed_username = request.GET.get('followed_username', None)

    follower = get_object_or_404(User, username=follower_username)
    followed = get_object_or_404(User, username=followed_username)
    takip_ediyor_mu = Following.kullaniciyi_takip_ediyor_mu(follower=follower,followed=followed)

    if not takip_ediyor_mu:
        Following.kullanici_takip_et(follower=follower, followed=followed)
        data.update({'msg': 'Takipten Çıkar'})
    else:
        Following.kullaniciyi_takipten_cikar(follower=follower, followed=followed)
        data.update({'msg':'Takip Et'})

    takipci_ve_takip_edilen_sayisi = Following.kullaniciyi_takip_edilenler_ve_takipciler(followed)
    context = {'takipciler':takipci_ve_takip_edilen_sayisi['takipciler'],
               'takip_edilenler':takipci_ve_takip_edilen_sayisi['takip_edilenler']}
    html = render_to_string('auth/profile/include/following_partion.html',context=context, request=request)
    data.update({'html':html})
    return JsonResponse(data=data)
