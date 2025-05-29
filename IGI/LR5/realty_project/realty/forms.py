from django import forms
from .models import Property, Agent, Review


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['agent'].queryset = Agent.objects.all()


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({'class': 'form-control'})
        self.fields['text'].widget.attrs.update({'class': 'form-control', 'rows': 4})