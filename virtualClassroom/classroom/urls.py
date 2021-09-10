from django.urls import path
from . import views



urlpatterns = [
    path('',views.viewsAssign.as_view()),
    path('create/',views.CURDbyTeacher.as_view()),
    path('update/<int:pk>',views.CURDbyTeacher.as_view()),
    path('delete/<int:pk>',views.CURDbyTeacher.as_view()),
    path('<int:pk>',views.viewsAssign.as_view()),
    # path('getassign/<int:pk>',views.studentView.as_view()),
    path('submit/<int:pk>',views.assigmentSubmitted.as_view()),

]