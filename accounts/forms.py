from django import forms
from connect_redis import get_client
redis_ob = get_client()

class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput(render_value=False))

    def clean_email(self):
        user = redis_ob.exists("user:email:%s" %md5_constructor(self.cleaned_data['email']))
        if user:
            raise forms.ValidationError("Email already exists")
        return self.cleaned_data['email']

    def save(self):
        pass