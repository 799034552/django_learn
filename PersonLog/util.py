
from django.http import HttpResponse, HttpRequest,HttpResponseRedirect
from django.urls import reverse
def get_error_message(err):
    """获取错误列表
    Args:
        err (_type_): 错误
    Returns:
        res: 包含错误信息的列表
    """
    res = []
    for value in err.values():
        res.extend(value)
    return "\\n".join(res)

def back(request, default = "PersonLog:PersonList"):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse(default)))
    