from django import forms

from vehicle.models import Vehicle
from .models import SparePartType, SparePart, Attribute, SparePartImage


class SparePartForm(forms.ModelForm):
    class Meta:
        model = SparePart
        fields = ['spare_part_type', 'vehicle', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['spare_part_type'].queryset = SparePartType.objects.filter(is_deleted=False)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(is_deleted=False)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.Select):
                widget.attrs['class'] = 'form-select'
            else:
                widget.attrs['class'] = 'form-control'


class SparePartImageForm(forms.ModelForm):
    class Meta:
        model = SparePartImage
        fields = ['file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].required = False


class SparePartTypeForm(forms.ModelForm):
    class Meta:
        model = SparePartType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Шина A235TO'}),
        }
        widgets['name'].attrs['class'] = 'form-control'


class AttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = ['name', 'unit', 'data_type']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Диаметр'}),
            'unit': forms.TextInput(attrs={'placeholder': 'мм'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.Select):
                widget.attrs['class'] = 'form-select'
            else:
                widget.attrs['class'] = 'form-control'


class AttributeValueForm(forms.Form):
    attribute_id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    attribute_name = forms.CharField(required=False, label='Атрибут', disabled=True)
    is_selected = forms.BooleanField(required=False, label='Добавить')
    value = forms.CharField(required=False, label='Значение')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            elif isinstance(widget, forms.HiddenInput):
                continue
            elif name == 'attribute_name':
                widget.attrs['class'] = 'form-control-plaintext'
            else:
                widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('is_selected') and not cleaned_data.get('value'):
            raise forms.ValidationError('Указанный атрибут требует значения.')
        return cleaned_data
