from django import forms
from django.contrib.auth.models import User
from .models import Category, Page, UserProfile, Article, Edit


class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # provide an association between the ModelForm and a model.
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(
        max_length=128, help_text='Please enter the title of the page.')
    url = forms.URLField(
        max_length=200, help_text='Please enter the URL of the pag.')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # If url is not empty and doesn't startwith 'http://', prepend
        # 'http://'
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
        return cleaned_data

    class Meta:
        model = Page

        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form
        # exclude = ('category')
        # or specify the fields to include
        fields = ('title', 'url', 'views')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile

        fields = ('website', 'picture')




class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        # fields = ('',)
        exclude = ['author', 'slug']


class EditForm(forms.ModelForm):
    class Meta:
        model = Edit
        fields = ['summary']
    

    
