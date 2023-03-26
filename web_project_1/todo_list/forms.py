from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ("title", "description", "start_date",
                  "end_date", "important", "complete")  # "__alt__"
