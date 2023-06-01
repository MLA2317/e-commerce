from rest_framework import serializers
from ..models import Contact, Subscribe


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'name', 'email', 'message', 'created_date')
        extra_kwargs = {
            'created_date': {'read_only': True}
        }
