from django import forms

from users.models import User


class UserForm(forms.Form):
    username = forms.CharField(required=True,
                               error_messages={
                                   'required': '用户名不能为空',
                                   'max_length': '用户名不能超过20个字符',
                               })
    password = forms.CharField(required=True,
                               error_messages={
                                   'required': '密码不能为空',
                               })
    mobile = forms.CharField(error_messages={
                                'max_length': '手机号最多11位'
                            })

    def clean(self):
        # 校验用户名是否已经注册过
        user = User.objects.filter(username=self.cleaned_data.get('username'))
        if user:
            # 已经注册
            raise forms.ValidationError({'username': '用户名已存在'})
        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(required=True,
                               error_messages={
                                   'required': '用户名不能为空',
                               })
    password = forms.CharField(required=True,
                               error_messages={
                                   'required': '密码不能为空',
                               })