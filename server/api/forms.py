from django import forms

from api.models import Vehicle


class VehicleForm(forms.ModelForm):
    number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Номер ТС')
    rent_status = forms.CharField(
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}, choices=Vehicle.rent_choice),
        label='Статус аренды'
    )
    is_online = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': "form-check-input"}), initial=True, required=False, label='Статус онлайн')
    options = forms.JSONField(widget=forms.Textarea(attrs={'class': 'form-control'}), initial={}, label='Свойства ТС')

    class Meta:
        model = Vehicle
        fields = ['number', 'rent_status', 'is_online', 'options']


class SetOptionsForm(forms.ModelForm):
    options = forms.JSONField(widget=forms.Textarea(attrs={'class': 'form-control'}), label='Свойства ТС', initial={})

    class Meta:
        model = Vehicle
        fields = ['options']


class SetRentStatusForm(forms.ModelForm):
    rent_status = forms.CharField(
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}, choices=Vehicle.rent_choice),
    )

    class Meta:
        model = Vehicle
        fields = ['rent_status']


class SetOnlineStatusForm(forms.ModelForm):
    YES_NO = (
        (True, 'Онлайн'),
        (False, 'Оффлайн'),
    )
    is_online = forms.TypedChoiceField(
        choices=YES_NO,
        widget=forms.RadioSelect,
        label='Статус онлайн',
        initial=True
    )

    class Meta:
        model = Vehicle
        fields = ['is_online']
