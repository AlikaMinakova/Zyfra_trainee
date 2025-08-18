from django.utils.timezone import now
from django.views.generic import CreateView, View, UpdateView, DeleteView, ListView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from .models import SparePartType, SparePart, SparePartImage, Attribute, AttributeValue, SparePartLog

from .forms import SparePartTypeForm, SparePartForm, SparePartImageForm, AttributeForm, AttributeValueForm
from django.db import transaction
from django.forms import inlineformset_factory, formset_factory


class SparePartCreateView(CreateView):
    model = SparePart
    form_class = SparePartForm
    template_name = 'spare_part/spare_part_form.html'
    success_url = reverse_lazy('spare_part:spare_part_list')

    def form_valid(self, form):
        self.object = form.save()
        message = (
            f"Создано: "
            f"Техника – '{getattr(self.object, 'vehicle', '-')}', "
            f"Тип запчасти – '{getattr(self.object, 'spare_part_type', '-')}', "
            f"Статус – '{getattr(self.object, 'get_status_display', lambda: '-')()}'"
        )

        SparePartLog.objects.create(spare_part=self.object, message=message)
        return redirect(self.success_url)


class SparePartUpdateView(UpdateView):
    model = SparePart
    form_class = SparePartForm
    template_name = 'spare_part/spare_part_form.html'
    success_url = reverse_lazy('spare_part:spare_part_list')

    def form_valid(self, form):
        old_instance = self.get_object()
        old_values = {
            'vehicle': old_instance.vehicle,
            'spare_part_type': old_instance.spare_part_type,
            'status': old_instance.status,
        }

        self.object = form.save()

        new_values = {
            'vehicle': self.object.vehicle,
            'spare_part_type': self.object.spare_part_type,
            'status': self.object.status,
        }

        changes = []
        for field, old_value in old_values.items():
            new_value = new_values[field]
            if old_value != new_value:
                if field == 'status':
                    old_display = old_instance.get_status_display()
                    new_display = self.object.get_status_display()
                    changes.append(f"поле {field}: '{old_display}' заменено на '{new_display}'")
                else:
                    changes.append(f"поле {field}: '{old_value}' заменено на '{new_value}'")

        if changes:
            message = f"Обновлено: " + ", ".join(changes)
            SparePartLog.objects.create(spare_part=self.object, message=message)

        return redirect(self.success_url)


class SparePartDetailView(DetailView):
    model = SparePart
    template_name = 'spare_part/spare_part_detail.html'
    context_object_name = 'spare_part'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        spare_part = self.object
        spare_part_type = spare_part.spare_part_type

        images = spare_part_type.images.filter(is_deleted=False)
        context['spare_part_images'] = images

        context['change_logs'] = spare_part.change_logs.order_by('-timestamp')

        attribute_values = AttributeValue.objects.filter(spare_part_type=spare_part_type).select_related('attribute')
        attributes_with_values = [
            {
                'name': av.attribute.name,
                'unit': av.attribute.unit,
                'value': av.value
            }
            for av in attribute_values
        ]
        context['attributes'] = attributes_with_values

        return context


class SparePartListView(ListView):
    model = SparePart
    template_name = 'spare_part/spare_part_list.html'
    context_object_name = 'spare_parts'
    paginate_by = 10
    queryset = SparePart.objects.filter(is_deleted=False)


class SparePartDeleteView(View):
    def post(self, request, pk):
        with transaction.atomic():
            spare_part = get_object_or_404(SparePart, pk=pk)
            spare_part.is_deleted = True
            spare_part.save()

            SparePartLog.objects.filter(spare_part=spare_part).update(is_deleted=True)
        return redirect('spare_part:spare_part_list')


class SparePartTypeCreateView(CreateView):
    model = SparePartType
    form_class = SparePartTypeForm
    template_name = 'spare_part/spare_part_type_form.html'
    success_url = reverse_lazy('spare_part:spare_part_type_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        AttributeValueFormSet = formset_factory(AttributeValueForm, extra=0)
        ImageFormSet = inlineformset_factory(
            SparePartType, SparePartImage,
            form=SparePartImageForm,
            extra=3,
            can_delete=False
        )
        if self.request.method == 'POST':
            context['image_formset'] = ImageFormSet(self.request.POST, self.request.FILES)
            context['attribute_formset'] = AttributeValueFormSet(self.request.POST)
        else:
            context['image_formset'] = ImageFormSet()
            initial = [
                {'attribute_id': a.id, 'attribute_name': a.name}
                for a in Attribute.objects.all()
            ]
            context['attribute_formset'] = AttributeValueFormSet(initial=initial)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context.get('image_formset')
        attribute_formset = context.get('attribute_formset')
        if image_formset.is_valid() and attribute_formset.is_valid():
            self.object = form.save()
            if image_formset:
                image_formset.instance = self.object
                images = image_formset.save(commit=False)
                for image in images:
                    if image.file:
                        image.save()

            for form_data in attribute_formset.cleaned_data:
                if form_data.get('is_selected'):
                    AttributeValue.objects.create(
                        attribute_id=form_data['attribute_id'],
                        spare_part_type=self.object,
                        value=form_data['value']
                    )
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)


class SparePartTypeUpdateView(UpdateView):
    model = SparePartType
    form_class = SparePartTypeForm
    template_name = 'spare_part/spare_part_type_form.html'
    success_url = reverse_lazy('spare_part:spare_part_type_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True

        AttributeValueFormSet = formset_factory(AttributeValueForm, extra=0)
        ImageFormSet = inlineformset_factory(
            SparePartType, SparePartImage,
            form=SparePartImageForm,
            extra=3,
            can_delete=True
        )

        if self.request.method == 'POST':
            context['image_formset'] = ImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
            context['attribute_formset'] = AttributeValueFormSet(self.request.POST)
        else:
            # Атрибуты
            existing_attrs = {
                val.attribute_id: val
                for val in AttributeValue.objects.filter(spare_part_type=self.object, is_deleted=False)
            }

            initial = []
            for attr in Attribute.objects.all():
                attr_val = existing_attrs.get(attr.id)
                initial.append({
                    'attribute_id': attr.id,
                    'attribute_name': attr.name,
                    'value': attr_val.value if attr_val else '',
                    'is_selected': bool(attr_val)
                })

            context['attribute_formset'] = AttributeValueFormSet(initial=initial)
            context['image_formset'] = ImageFormSet(
                instance=self.object,
                queryset=SparePartImage.objects.filter(spare_part_type=self.object, is_deleted=False)
            )

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context.get('image_formset')
        attribute_formset = context.get('attribute_formset')
        if (not image_formset or image_formset.is_valid()) and attribute_formset.is_valid():
            self.object = form.save()

            for image_form in image_formset:
                image = image_form.instance

                if image_form.cleaned_data.get('DELETE'):
                    if image.pk:
                        image.is_deleted = True
                        image.save()

                elif not image.pk and image_form.cleaned_data.get('file'):
                    image.vehicle = self.object
                    image.save()

            AttributeValue.objects.filter(spare_part_type=self.object).update(is_deleted=True)

            for form_data in attribute_formset.cleaned_data:
                if form_data.get('is_selected'):
                    AttributeValue.objects.update_or_create(
                        attribute_id=form_data['attribute_id'],
                        spare_part_type=self.object,
                        defaults={
                            'value': form_data['value'],
                            'is_deleted': False,
                        }
                    )
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)


class SparePartTypeListView(ListView):
    model = SparePartType
    template_name = 'spare_part/spare_part_type_list.html'
    context_object_name = 'spare_part_types'
    queryset = SparePartType.objects.filter(is_deleted=False)


class SparePartTypeDeleteView(View):
    def post(self, request, pk):
        with transaction.atomic():
            spare_part_type = get_object_or_404(SparePartType, pk=pk)
            spare_part_type.is_deleted = True
            spare_part_type.save()

            SparePart.objects.filter(spare_part_type=spare_part_type).update(is_deleted=True)

            SparePartImage.objects.filter(spare_part_type=spare_part_type).update(is_deleted=True)

            AttributeValue.objects.filter(spare_part_type=spare_part_type).update(is_deleted=True)
        return redirect('spare_part:spare_part_type_list')


class AttributeCreateView(CreateView):
    model = Attribute
    form_class = AttributeForm
    template_name = 'spare_part/attribute_form.html'
    success_url = reverse_lazy('spare_part:attribute_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        return context


class AttributeUpdateView(UpdateView):
    model = Attribute
    form_class = AttributeForm
    template_name = 'spare_part/attribute_form.html'
    success_url = reverse_lazy('spare_part:attribute_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        context['instance'] = self.object
        return context


class AttributeListView(ListView):
    model = Attribute
    template_name = 'spare_part/attribute_list.html'
    context_object_name = 'attributes'
    paginate_by = 10
    queryset = Attribute.objects.filter(is_deleted=False)


class AttributeDeleteView(View):
    def post(self, request, pk):
        with transaction.atomic():
            attribute = get_object_or_404(Attribute, pk=pk)
            attribute.is_deleted = True
            attribute.save()

            AttributeValue.objects.filter(attribute=attribute).update(is_deleted=True)

        return redirect('spare_part:attribute_list')
