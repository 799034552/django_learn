from django.urls import path, re_path

from . import views
app_name = "PersonLog"

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('Login', views.Login.as_view(), name="Login"),
    path('PersonList', views.PersonList.as_view(), name="PersonList"),
    path('PersonAdd', views.PersonAdd.as_view(), name="PersonAdd"),
    path('PersonDel/<int:id>', views.PersonDel.as_view(), name="PersonDel"),
    path('PersonModify/<int:id>', views.PersonModify.as_view(), name="PersonModify"),
]