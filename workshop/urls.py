"""workshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from room_booking_app import views as vw

urlpatterns = [
    path('admin/', admin.site.urls),
    path('room/new/', vw.new_room ),
    path('all-rooms/', vw.all_rooms),
    path('room-details/<int:room_id>', vw.room_details),
    path('room-modify/<int:room_id>', vw.room_modify),
    path('room-delete/<int:room_id>', vw.room_delete),
    path('room-reserve/<int:room_id>', vw.room_reserve),
    path('room-search/', vw.room_search),
]
