
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, AuthenticationForm, SetPasswordForm
from .models import StudentUser, Enrolled_Students, TeacherUser
from django.forms import ModelForm
from django.forms.widgets import DateInput, PasswordInput
from string import ascii_letters, digits as num_digits
from secrets import choice
from captcha.fields import CaptchaField
from .auth_backends import TeacherAuthenticationBackend


class CustomCreationForm(UserCreationForm):
    """
    Defines a custom creation form for the `StudentUser` model in Django.

    CustomCreationForm:
        A subclass of `UserCreationForm` that provides a custom implementation for the `save` method.
        It includes additional fields and widgets for the `StudentUser` model, such as the `lrn`, `grade_year`, and `image_id`.
        It also sets the `is_active` flag of the user to False when the form is saved. This is for initial account activation.
        Parameters:
            - commit: A boolean value indicating whether to save the form data to the database or not.
        Raises:
            - None.
    """
    
    class Meta(UserCreationForm.Meta):
        model = StudentUser
        fields = ('lrn', 'last_name', 'first_name', 'grade_year', 'birthday', 'age', 'username', 'email', 'parent_email', 'image_id', 'enrollment_status', 'password1', 'password2', 'data_privacy_agreed', 'terms_agreed')
        widgets = {
            'birthday': DateInput(attrs={
                'type' : 'date',
                'placeholder': 'YYYY-MM-DD'
            }),
            'image_id': forms.ClearableFileInput(attrs={'multiple': True}),
            'data_privacy_agreed': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                
                }),
            'terms_agreed' : forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            })
        }
        enctype = 'multipart/form-data'

    def save(self, commit=True):
            user = super().save(commit=False)
            user.is_active = False  # Set is_active to False
            if commit:
                user.save()
            return user

        

"""
Defines two classes `CustomerUserChangeForm` and `StudentInfoForm`, both of which are subclasses of `UserChangeForm` and `ModelForm` respectively.

CustomerUserChangeForm:
    A subclass of `UserChangeForm` that provides a custom implementation for the `Meta` class.
    It includes fields such as `lrn`, `last_name`, `first_name`, `email`, `birthday`, `grade_year`, and `strand` for the `StudentUser` model.
    Parameters:
        - None.
    Raises:
        - None.

StudentInfoForm:
    A subclass of `ModelForm` that provides a custom implementation for the `Meta` class.
    It includes fields such as `lrn`, `last_name`, `first_name`, `age`, `birthday`, `email`, `grade_year`, `section`, and `strand` for the `StudentUser` model.
    Parameters:
        - None.
    Raises:
        - None.
"""


class CustomerUserChangeForm(UserChangeForm):

    class Meta:
        model = StudentUser
        fields = ('lrn', 'last_name', 'first_name', 'email', 'birthday', 'grade_year', 'strand')



class StudentInfoForm(ModelForm):
    class Meta:
        model = StudentUser
        fields = 'lrn', 'last_name', 'first_name', 'age', 'birthday', 'email', 'grade_year', 'section', 'strand'




class TeacherCreationForm(UserCreationForm):

    class Meta:
        model = StudentUser
        fields = ['lrn', 'last_name', 'first_name', 'username', 'email', 'password1', 'password2']
        

    def __init__(self, *args, **kwargs):
        form = super().__init__(*args, **kwargs)
        print(form)
        alphabet = ascii_letters + num_digits
        self.sys_pass = ''.join(choice(alphabet) for i in range(15))
        print(self.sys_pass)
        self.fields['password1'].initial = self.sys_pass
        self.fields['password2'].initial = self.sys_pass
        

    def save(self, commit=True):
        print('save method called')
        user = super().save(commit=False)
        
        if commit:
            user.username = f"DepEd_{user.username}"
            user.set_password(self.sys_pass)
            print(user)
            user.save()
            teacher_user = TeacherUser.objects.create(
                user_field=user,
                teacher_id=f"DepEd_{user.lrn}",
                first_name=user.first_name,
                last_name=user.last_name,
                raw_password = self.sys_pass
            )
            print(teacher_user)
            teacher_user.save()
        return user




class TeacherLogInForm(AuthenticationForm):
    teacher_id = forms.CharField(max_length=20)
    captcha = CaptchaField()
    print('called form')

    def clean(self):
        cleaned_data = super().clean()
        teacher_id = cleaned_data.get('teacher_id')
        print(teacher_id)
        username = cleaned_data.get('username')
        print(username)
        password = cleaned_data.get('password')
    
        User = get_user_model()

        try:
            teacher_user = TeacherUser.objects.get(teacher_id=teacher_id)
            print(teacher_user)
            user = teacher_user.user_field
        except TeacherUser.DoesNotExist:
            raise forms.ValidationError(
                "Invalid login credentials. Please try again.",
                code='invalid_login'
            )

        user = authenticate(teacher_id=teacher_id, username=username, password=password)
        
        if user is None:
            raise forms.ValidationError(
                "Invalid login credentials. Please try again.",
                code='invalid_login',
            )
        
        if teacher_user.teacher_id != teacher_id:
            raise forms.ValidationError(
                "Invalid login credentials. Please try again.",
                code='invalid_login',
            )
        
        return cleaned_data
    


class TeacherChangeDetailsForm(UserChangeForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
        self.fields['password'].help_text = "Enter a new password only if you want to change it."



    class Meta:
        model = StudentUser
        fields = ['username', 'password']
        widgets = {
            'password' : PasswordInput(render_value=False, attrs={ 'class' : 'form-control'})

        }


    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["username"]
        if commit:
            user.save()
        return user
    


class ResetPasswordForm(SetPasswordForm):
    
    class Meta:
        model = StudentUser
        fields = ['new_password', 'new_password_confirm']