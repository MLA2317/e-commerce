from django.shortcuts import render
from .models import Profile


def profile(request):
    pf = Profile.objects.get(user=request.user)
    print(pf)
    ctx = {
        'profile': pf
    }
    return render(request, 'profile/profile.html', ctx)
