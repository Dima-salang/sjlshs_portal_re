from django import forms
from .models import GoodMoral


class GoodMoralForm(forms.ModelForm):
    class Meta:
        model = GoodMoral
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['full_name'].initial = user
            

            self.fields['grade_level'].initial = user.grade_year
          

            self.fields['lrn'].initial = user.lrn
         

            self.fields['email'].initial = user.email
            

    def clean(self):
        cleaned_data = super().clean()
        # Exclude required validation for pre-populated fields
        self.fields['full_name'].required = False
        self.fields['grade_level'].required = False
        self.fields['lrn'].required = False
        self.fields['email'].required = False
        return cleaned_data
    

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.full_name_id is None:
            instance.full_name_id = self.fields['full_name'].initial.id
            
        if commit:
            instance.save()
        return instance
