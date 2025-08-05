from django import forms

from .models import Vehicle, VehicleImage, VehicleType


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'reg_number', 'brand', 'date_purchase', 'type',
            'mileage', 'operation_status'
        ]
        widgets = {
            'reg_number': forms.TextInput(attrs={'placeholder': 'A123BC'}),
            'brand': forms.TextInput(attrs={'placeholder': 'УРАЛ'}),
            'date_purchase': forms.DateInput(attrs={'type': 'date'}),
            'mileage': forms.NumberInput(attrs={'placeholder': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].queryset = VehicleType.objects.filter(is_deleted=False)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.Select):
                widget.attrs['class'] = 'form-select'
            else:
                widget.attrs['class'] = 'form-control'


class VehicleImageForm(forms.ModelForm):
    class Meta:
        model = VehicleImage
        fields = ['file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].required = False


class VehicleTypeForm(forms.ModelForm):
    class Meta:
        model = VehicleType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Трактор'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            widget.attrs['class'] = 'form-control'


class VehicleFilterForm(forms.Form):
    brand = forms.CharField(label='Бренд', required=False)
