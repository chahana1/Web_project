from django import forms
from board.models import Care, Comment, ReComment


class CareForm(forms.ModelForm):
    class Meta:
        model = Care
        fields = ["title", "place", "content", "image"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['contents']
