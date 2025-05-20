from django import forms
from .models import Message, FileTransfer
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class MessageForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(
        queryset=User.objects.none(),  # we'll override this in __init__
        label="Send to"
    )

    class Meta:
        model = Message
        fields = ['receiver', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['receiver'].queryset = User.objects.exclude(id=user.id)


class FileTransferForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(
        queryset=User.objects.none(),  # override in __init__
        label="Send file to"
    )

    class Meta:
        model = FileTransfer
        fields = ['receiver', 'file']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['receiver'].queryset = User.objects.exclude(id=user.id)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
