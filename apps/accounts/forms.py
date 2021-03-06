import random
from django import forms
from django.utils.hashcompat import md5_constructor, sha_constructor
from connect_redis import get_client
redis_ob = get_client()

def generate_api_key(user_email):
    api_key = md5_constructor("%s%s" %(str(user_email), str(random.random()))).hexdigest()
    while redis_ob.exists("user:api_key:%s" %api_key):
        api_key = md5_constructor("%s%s" %(str(user_email), str(random.random()))).hexdigest()
    return api_key

def generate_password(password):
    # generating salt. Trying to mimic django auth app password generation
    salt = sha_constructor(str(random.random()) +str(random.random())).hexdigest()[:5]
    hsh = sha_constructor(salt + password).hexdigest()
    return salt, hsh

class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput(render_value=False))

    def clean_email(self):
        if redis_ob.exists("user:email:%s" %md5_constructor(self.cleaned_data['email']).hexdigest()):
            raise forms.ValidationError("Email already exists")
        return self.cleaned_data['email']

    def save(self):
        # get the user id by incrementing counter
        user_id = redis_ob.incr("counter:user")
        salt, hsh = generate_password(self.cleaned_data["password"])
        # using redis pipeline to make it happen as a transaction.
        redis_pipe = redis_ob.pipeline()
        api_key = generate_api_key(self.cleaned_data['email'])
        redis_pipe.set("user:email:%s" %md5_constructor(self.cleaned_data['email']).hexdigest(), user_id)\
                  .hmset("user:%d" %user_id, {"email": self.cleaned_data["email"], 
                                              "password": "%s$%s" %(salt, hsh), 
                                              "api_key":api_key})\
                  .set("user:api_key:%s" %(api_key), user_id)
        redis_pipe.execute()
        return user_id


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput(render_value=False))

    # checking if email and password matches
    def clean(self):
        if self.cleaned_data.has_key('email') and self.cleaned_data.has_key('password'):
            # check if email exists
            user_id = redis_ob.get("user:email:%s" %md5_constructor(self.cleaned_data['email']).hexdigest())
            if not user_id:
                raise forms.ValidationError("Invalid user credentials")
            # now check if the password matches
            user_password = redis_ob.hget("user:%s" %user_id, "password")
            # mimic the django auth password match code
            salt, hsh = user_password.split("$")
            if not hsh == sha_constructor(salt + self.cleaned_data['password']).hexdigest():
                raise forms.ValidationError("Invalid user credentials")
        return self.cleaned_data

class SettingsForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=False, widget=forms.PasswordInput(render_value=False))
    custom_domain = forms.CharField(required=False, help_text="<a href='#custom_domain' rel='facebox' class='custom_domain'>help</a>")

    def clean_custom_domain(self):
        custom_domain = self.cleaned_data['custom_domain']
        if custom_domain and not '.' in custom_domain:
            raise forms.ValidationError("Does n't look like a domain to me")
        return custom_domain
            

