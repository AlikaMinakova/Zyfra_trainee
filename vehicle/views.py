from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, View

from .forms import VehicleForm, VehicleImageForm, VehicleFilterForm
from .forms import VehicleTypeForm
from .models import Vehicle, VehicleImage, VehicleType


class VehicleCreateView(CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'vehicle/vehicle_form.html'
    success_url = reverse_lazy('vehicle:vehicle_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ImageFormSet = inlineformset_factory(
            Vehicle, VehicleImage,
            form=VehicleImageForm,
            extra=3,
            can_delete=False
        )
        if self.request.method == 'POST':
            context['image_formset'] = ImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['image_formset'] = ImageFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']

        if image_formset.is_valid():
            self.object = form.save()
            image_formset.instance = self.object

            images = image_formset.save(commit=False)

            for image in images:
                if image.file:
                    image.save()

            return redirect(self.success_url)
        else:
            return self.form_invalid(form)


class VehicleUpdateView(UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'vehicle/vehicle_form.html'
    success_url = reverse_lazy('vehicle:vehicle_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ImageFormSet = inlineformset_factory(
            Vehicle, VehicleImage,
            form=VehicleImageForm,
            extra=3,
            can_delete=True
        )
        if self.request.method == 'POST':
            context['image_formset'] = ImageFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.object
            )
        else:
            context['image_formset'] = ImageFormSet(
                instance=self.object,
                queryset=VehicleImage.objects.filter(vehicle=self.object, is_deleted=False)
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']

        if image_formset.is_valid():
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

            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)


class VehicleDetailView(DetailView):
    model = Vehicle
    template_name = 'vehicle/vehicle_detail.html'
    context_object_name = 'vehicle'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = self.object.images.filter(is_deleted=False)
        return context


class VehicleListView(ListView):
    model = Vehicle
    template_name = 'vehicle/vehicle_list.html'
    context_object_name = 'vehicles'
    paginate_by = 10

    def get_queryset(self):
        qs = Vehicle.objects.filter(is_deleted=False)
        brand = self.request.GET.get('brand')
        if brand:
            qs = qs.filter(brand__icontains=brand)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = VehicleFilterForm(self.request.GET or None)
        return context


class VehicleDeleteView(View):
    def post(self, request, pk):
        with transaction.atomic():
            vehicle = get_object_or_404(Vehicle, pk=pk)
            vehicle.is_deleted = True
            vehicle.save()
            VehicleImage.objects.filter(vehicle=vehicle).update(is_deleted=True)
        return redirect('vehicle:vehicletype_list')


class VehicleTypeCreateView(CreateView):
    model = VehicleType
    form_class = VehicleTypeForm
    template_name = 'vehicle/vehicletype_form.html'
    success_url = reverse_lazy('vehicle:vehicletype_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        return context


class VehicleTypeUpdateView(UpdateView):
    model = VehicleType
    form_class = VehicleTypeForm
    template_name = 'vehicle/vehicletype_form.html'
    success_url = reverse_lazy('vehicle:vehicletype_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        context['instance'] = self.object
        return context


class VehicleTypeListView(ListView):
    model = VehicleType
    template_name = 'vehicle/vehicletype_list.html'
    context_object_name = 'types'
    paginate_by = 10

    def get_queryset(self):
        return VehicleType.objects.filter(is_deleted=False)


class VehicleTypeDeleteView(View):
    def post(self, request, pk):
        with transaction.atomic():
            vehicle_type = get_object_or_404(VehicleType, pk=pk)
            vehicle_type.is_deleted = True
            vehicle_type.save()

            vehicles = Vehicle.objects.filter(type=vehicle_type)
            vehicles.update(is_deleted=True)

            VehicleImage.objects.filter(vehicle__in=vehicles).update(is_deleted=True)
        return redirect('vehicle:vehicletype_list')
