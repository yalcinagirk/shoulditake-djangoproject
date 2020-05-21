from django import forms
from app.models import Product, Comment
from ckeditor.widgets import CKEditorWidget


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'icerik', 'image', 'categorys', 'Subcategorys', 'ProductTitles']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}

    def clean_icerik(self):
        icerik = self.cleaned_data.get('icerik')

        if len(icerik) < 250:
            raise forms.ValidationError('İcerik en az 250 karakterden oluşmalıdır.%s' % len(icerik))
        return icerik


class CategorySorguForm(forms.Form):
    # Category = (('all', 'HEPSİ'), ('elektronik', 'Elektronik'), ('moda', 'MODA'))
    search = forms.CharField(required=False, max_length=500, widget=forms.TextInput(
        attrs={'placeholder': 'Bir şeyler arayınız.', 'class': 'form-control'}))
    # taslak_yayin = forms.ChoiceField(label='', widget=forms.Select(attrs={'class': 'form-control'}),Zchoices=Category, required=True)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['icerik']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
