from django import forms

from .models import BlogPost


class PostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "text"]
        Widget = {"text": forms.Textarea(attrs={"cols": 80})}
