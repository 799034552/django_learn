from django import forms

class UserForm(forms.Form):
    username = forms.CharField(max_length=255, error_messages={
        "required":"用户名不能为空",
        })
    passwd = forms.CharField(max_length=100, min_length=2,error_messages={
        "required":"密码不能为空",
        "min_length": "密码长度不能太小",
        "max_length": "密码长度不能太长",
        "invalid": "密码格式错误",
    })
    

def validate_file_size( MAX_FILE_SIZE_MB):
    # 将文件大小转换为字节
    def validate_file_size(value):
        max_size = MAX_FILE_SIZE_MB * 1024 * 1024
        if value.size > max_size:
            raise forms.ValidationError(f"文件大小不能超过 {MAX_FILE_SIZE_MB}MB")
    return validate_file_size


class PersonForm(forms.Form):
    name = forms.CharField(max_length=255, error_messages={
        "required":"姓名不能为空",
    })
    age = forms.IntegerField(min_value=0, max_value=200, required=False,error_messages={
        "invalid": "年龄格式错误",
    })
    pic = forms.ImageField(required=False, validators=[validate_file_size(20)])
    
