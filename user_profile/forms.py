from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'size': 32, 'placeholder': 'Enter Username.', 'class':'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'size': 32, 'placeholder': 'Enter email address', 'class':'form-control'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'size': 32, 'placeholder': 'Enter Password', 'class':'form-control'}))
    confirm_password = forms.CharField(widget=forms.TextInput(attrs={'size': 32, 'placeholder': 'Confirm Password', 'class':'form-control'}))

    def clean(self):
        password = self.cleaned_data.get('password', None)
        cpassword = self.cleaned_data.get('confirm_password', None)
        if password and cpassword and (password == cpassword):
            return self.cleaned_data
        else:
            raise forms.ValidationError("Passwords don't match")
