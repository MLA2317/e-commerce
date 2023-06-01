from rest_framework import generics, status, permissions
from .serialziers import ContactSerializer
from ..models import Contact


class ContactCreateView(generics.ListCreateAPIView):
    # http://127.0.0.1:8000/contact/api/create/
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


