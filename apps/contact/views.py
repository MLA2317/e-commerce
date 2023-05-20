from django.shortcuts import render
from .models import Contact, Subscribe
from .forms import ContactForm
from apps.products.models import Category


def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.save()
    email = request.GET.get('email')
    if email:
        Subscribe.objects.create(email=email)
    ctx = {
        'form': form,
    }
    return render(request, 'product/contact.html', ctx)
