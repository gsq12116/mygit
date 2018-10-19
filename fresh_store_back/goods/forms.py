from django import forms


class GoodForm(forms.Form):
    name = forms.CharField(required=True,
                           error_messages={'required': '请输入商品名称'})
    goods_brief = forms.CharField(required=True,
                                  error_messages={'required': '请输入商品的简短描述',
                                                  'max_length': '简短描述不能多于500字符'})
    goods_sn = forms.CharField(required=True,
                               error_messages={'required': '请输入商品的简短描述',
                                               'max_length': '简短描述不能多于500字符'})
    category = forms.CharField(required=True,
                               error_messages={'required': '请输入商品的简短描述',
                                               'max_length': '简短描述不能多于500字符'})