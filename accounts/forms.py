import random
from django import forms
from django.utils.hashcompat import md5_constructor, sha_constructor
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
        # get the user id by incrementing counter
        user_id = redis_ob.incr("counter:user")
        # generating salt. Trying to mimic django auth app password generation
        salt = sha_constructor(str(random.random()) +str(random.random())).hexdigest()[:5]
        hsh = sha_constructor(str(random.random()) +self.cleaned_data["password"]).hexdigest()
        # using redis pipeline to make it happen as a transaction.
        redis_pipe = redis_ob.pipeline()
        redis_pipe.set("user:email:%s" %md5_constructor(self.cleaned_data['email']).hexdigest(), user_id).hmset("user:%d" %user_id, {"email": self.cleaned_data["email"], "password": "%s$%s" %(salt, hsh)})
        redis_pipe.execute()
        return user_id


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput(render_value=False))

    # checking if email and password matches
    def clean(self):
        # check if email exists
        user_id = redis_ob.get("user:email:%s" %md5_constructor(self.cleaned_data['email']))
        if not user_id:
            raise forms.ValidationError("Invalid user credentials")
        # now check if the password matches
        user_password = redis_ob.hget("user:%d" %user_id, "password")
        # mimic the django auth password match code
        salt, hsh = user_password.split("$")
        if not hsh == sha_constructor(salt, self.cleaned_data['password']):
            raise forms.ValidationError("Invalid user credentials")
        return self.cleaned_data
