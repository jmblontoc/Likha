from django import forms
from .models import STISurveillance, Maternal, HealthCareWasteManagement, InformalSettlers, UnemploymentRate


class MaternalForm(forms.ModelForm):

    class Meta:
        model = Maternal
        fields = '__all__'
        exclude = ('fhsis',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })


class STISurveillanceForm(forms.ModelForm):

    class Meta:
        model = STISurveillance
        fields = '__all__'
        exclude = ('fhsis',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })


class HealthCareWasteManagementForm(forms.ModelForm):

    class Meta:
        model = HealthCareWasteManagement
        fields = '__all__'
        exclude = ('date',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })


class InformalSettlersForm(forms.ModelForm):

    class Meta:
        model = InformalSettlers
        fields = '__all__'
        exclude =('date',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })


class UnemploymentRateForm(forms.ModelForm):

    class Meta:
        model = UnemploymentRate
        fields = '__all__'
        exclude = ('date',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })