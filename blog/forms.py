from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, widget=forms.TextInput(
        attrs={'class':'form-control'},))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class':'form-control'},))
    to = forms.EmailField(widget=forms.TextInput(
        attrs={'class':'form-control'}))
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control'}))



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

    # Read from the documentation
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['body'].widget.attrs.update({'class': 'form-control'})
        # widgets ={
        #     'name': forms.TextInput(attrs ={'class':'form-control'}),
        #     'email': forms.EmailField(attrs={'class': 'form-control'}),
        #     'body': forms.Textarea(attrs={'class': 'form-control'}),
        # }


class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Search....'}))
