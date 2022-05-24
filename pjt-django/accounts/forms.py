from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', )
        exclude= ('password',)        
        # 회원 정보 변경시 필드 고려하기
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):        
        model = get_user_model()
        fields = UserCreationForm.Meta.fields  
      