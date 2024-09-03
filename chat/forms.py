from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *

class GroupIsForm(ModelForm):
    class Meta:
        model = GroupIs
        exclude = ['host']  # Оставляем только exclude, fields не нужно

class MessageCreationForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        
        widgets = {
            'body': forms.TextInput(attrs={
                'placeholder': 'Add message ...',
                'class': 'p-1 text-black',
                'maxlength': '300',
                'autofocus': True,
                'style': 'width: 100%;',  # Устанавливает длину поля на 100% ширины контейнера
                
            }),
        }

        labels = {
            'body': '',  # Отключает отображение метки для поля body
        }



class MyUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=False, help_text='Optional.')

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'phone_number')  


class CustomAuthenticationForm(AuthenticationForm):
    # Здесь Meta не требуется, так как AuthenticationForm автоматически обрабатывает поля username и password.
    pass


from django import forms
from .models import MyUser 
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'phone_number'] 
