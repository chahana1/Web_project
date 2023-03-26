from django import forms
from .models import Volunteer,Organization


class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ["title", "organization", "content", "image","start_date","end_date"]

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = "__all__"
