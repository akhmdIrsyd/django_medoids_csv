from django import forms
from .models import upload_data


class Upload_dataForm(forms.ModelForm):

    class Meta:
        model = upload_data
        fields = [
            'isi',

        ]
