from .models import Review
from django import forms

class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        fields = ('content',)
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control', 'cols': 200, 'placeholder':'여기에 댓글을 작성해 주세요',})
        }