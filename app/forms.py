from django import forms
from app.models import Product


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
    Category = (('all', 'HEPSİ'), ('elektronik', 'Elektronik'), ('moda', 'MODA'))

    taslak_yayin = forms.ChoiceField(label='', widget=forms.Select(attrs={'class': 'form-control'}),
                                     choices=Category, required=True)
