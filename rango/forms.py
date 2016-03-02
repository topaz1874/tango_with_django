from django import forms
from django.contrib.auth.models import User
# from django.core.cache import cache
from .models import Category, Page, UserProfile, Article, Edit

from io import BytesIO
from PIL import Image, ImageDraw

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
    
class ImageForm(forms.Form):
    """Form to validate requested placeholder image."""
    height = forms.IntegerField(max_value=2000, min_value=1)
    width = forms.IntegerField(max_value=2000, min_value=1)

    def generate(self, image_format='PNG'):
        """generate an image of the given type and return as raw bytes."""
        height = self.cleaned_data['height']
        width = self.cleaned_data['width']

        key = '{}.{}.{}'.format(width, height, image_format)

        # content = cache.get(key)
        # if content is None:
        if key:
            image = Image.new('RGB',(width, height))
            draw = ImageDraw.Draw(image)
            text = '{} X {}'.format(width, height)
            textwidth, textheight = draw.textsize(text)
            if textwidth < width and textheight < height:
                texttop = (height-textheight)//2
                textleft =(width-textwidth)//2
                draw.text((textleft,texttop),text, fill=(255,255,255))
        content = BytesIO()
        image.save(content, image_format)
        content.seek(0)
        # cache.set(key, content, 60*60)
        return content 
    
