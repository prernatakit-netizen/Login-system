from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]


class FileUploadForm(forms.Form):

    file = forms.FileField()

    def clean_file(self):

        uploaded_file = self.cleaned_data['file']

        allowed_extensions = [
            '.pdf',
            '.doc',
            '.docx',
            '.txt',
            '.jpg',
            '.jpeg',
            '.png',
            '.gif',
            '.xls',
            '.xlsx',
            '.ppt',
            '.pptx',
            '.zip',
        ]

        file_name = uploaded_file.name.lower()

        if not any(
            file_name.endswith(extension)
            for extension in allowed_extensions
        ):
            raise forms.ValidationError(
                'This file type is not allowed.'
            )

        max_size = 5 * 1024 * 1024

        if uploaded_file.size > max_size:
            raise forms.ValidationError(
                'File size must be less than 5 MB.'
            )

        return uploaded_file


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email']


class ChangePasswordForm(PasswordChangeForm):

    class Meta:
        model = User