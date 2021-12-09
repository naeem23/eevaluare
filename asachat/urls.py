
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "asachat"
urlpatterns = [
    path('room/<int:id>/', views.chat_room, name="chat_room"),

]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
 