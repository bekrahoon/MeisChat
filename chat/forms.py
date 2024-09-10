from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *


class GroupIsForm(ModelForm):
    participants = forms.ModelMultipleChoiceField(queryset=MyUser.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'style': 'display: flex; flex-direction: column; align-items: flex-start;'}))
    class Meta:
        model = GroupIs
        exclude = ['host']  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.label != 'Participants':
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': field.label
                })


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
