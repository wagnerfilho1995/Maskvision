from django import forms
from .models import Amplifier, Document, Modelo, RequestPrediction

class FormControlClass(object):
    def __init__(self, *args, **kwargs):
        super(FormControlClass, self).__init__(*args, **kwargs)
        # you can iterate all fields here
        for fname, f in self.fields.items():
            f.widget.attrs['class'] = 'form-control'

class AmplifierForm(FormControlClass, forms.ModelForm):
    class Meta:
        fields = 'responsible', 'email', 'reference', 'mask'
        model = Amplifier

class DocumentForm(FormControlClass, forms.ModelForm):
    class Meta:
        #fields = 'description', 'document'
        fields = 'file_signal', 'file_h5', 'file_info'   
        model = Document

class ModeloForm(FormControlClass, forms.ModelForm):
    class Meta:
        fields = 'model_type', 'amplifier', 'file_h5', 'file_txt'
        model = Modelo

class RequestPredictionForm(FormControlClass, forms.ModelForm):
    class Meta:
        first_name = forms.CharField(error_messages={'required': 'Please let us know what to call you!'})
        fields = 'net_model', 'pin_signal', 'ganho'
        model = RequestPrediction
        widgets = {'ganho': forms.HiddenInput()}
