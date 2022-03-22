from django import forms
from .models import ChatMessage


class ChatMessageSaveForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = '__all__'