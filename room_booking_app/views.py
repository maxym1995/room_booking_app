from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
import random
from room_booking_app.models import *
import datetime



# add new room
def new_room(request):
    if request.method == "GET":
        return render(request,"new_room_template.html")
    if request.method == "POST":
        name = request.POST.get("room-name")
        capacity = request.POST.get("capacity")
        if request.POST.get("projector") == "on":
            projector = True
        else:
            projector = False
        rooms = Room.objects.all()
        rooms_names = []
        error_message=""
        for r in rooms:
            rooms_names.append(r.name)
        if name != "" and capacity != "":
            if name in rooms_names:
                error_message = "This name has been already used."
                return render(request, "new_room_template.html", context={"error_message": error_message})
            else:
                if int(capacity) > 0 and int(capacity) <=100:
                    Room.objects.create(name=name, capacity=capacity, projector_aval = projector)
                    return HttpResponseRedirect("/base")
                else:
                    error_message = "Capacity has to be number between 1 to 100."
                    return render(request, "new_room_template.html", context={"error_message": error_message})
        else:
            error_message = "Name and capacity have to be filled in."
            return render(request, "new_room_template.html", context={"error_message": error_message})


#display room details
def room_details(request,room_id):
    if request.method == "GET":
        room = Room.objects.get(id=room_id)
        reservation = Reservation.objects.all().filter(room_id_id=room_id).order_by("date")
        return render(request, "room_details.html", context={"room": room, "reservation":reservation })


#modify existing room
def room_modify(request,room_id):
    rooms = Room.objects.all()
    rooms_names = []
    for r in rooms:
        rooms_names.append(r.name)
    room = Room.objects.get(id=room_id)
    room_name = room.name
    rooms_names.pop(rooms_names.index(room_name))
    if request.method == "GET":
        room = Room.objects.get(id=room_id)
        return render(request, "modify_room.html",context={"room":room})
    if request.method == "POST":
        name = request.POST.get("room-name")
        capacity = request.POST.get("capacity")
        projector = bool(request.POST.get('projector'))
        error_message = ""
        if name != "" and int(capacity) >0 :
            if name in rooms_names:
                error_message = "This name has been already used."
                return render(request, "modify_room.html", context={"room":room, "error_message": error_message})
            else:
                room = Room.objects.get(id=room_id)
                room.name = name
                room.capacity = capacity
                room.projector_aval = projector
                room.save()
                return HttpResponseRedirect("/all-rooms/")
        else:
            error_message = "Name and capacity have to be filled in."
            return render(request, "modify_room.html", context={"error_message": error_message})



#delete exsisting room
def room_delete(request,room_id):
        room = Room.objects.get(id=room_id)
        room.delete()
        return HttpResponseRedirect("/all-rooms/")

#reserve exsiting room
def room_reserve(request,room_id):
    if request.method == "GET":
        room = Room.objects.get(id=room_id)
        todays = str(datetime.date.today())
        reservation = Reservation.objects.all().filter(room_id_id=room_id).order_by("date")
        return render(request, "reserve_room.html",context={"room":room, "todays":todays, "reservation":reservation})
    if request.method == "POST":
        room = Room.objects.get(id=room_id)
        today = str(datetime.datetime.today().strftime("%Y-%m-%d"))
        comment = request.POST.get("comment")
        date = request.POST.get("date")
        if Reservation.objects.filter(room_id=room_id, date=date):
            return render(request,"reserve_room.html", context={"room":room,"error":"This room is already booked"})
        if date < today:
            return render(request,"reserve_room.html", context={"room":room,"error":"This date is incorrect"})
        Reservation.objects.create(room_id_id=room_id, date=date, comment=comment)
        return HttpResponseRedirect("/all-rooms/")


#display list of all rooms (v2)
def all_rooms(request):
    if request.method == "GET":
        rooms = Room.objects.all().order_by("capacity")
        for room in rooms:
            reservation_dates = [reservation.date for reservation in room.reservation_set.all()]
            room.reserved = datetime.date.today() in reservation_dates
        if len(rooms) == 0:
            return HttpResponse("No rooms avaliable")
        else:
            return render(request, "all_roms_v2.html", context={"rooms": rooms})

# search for room with criterias
def room_search(request):
    if request.method == "GET":
        name = request.GET.get("room-name")
        capacity = request.GET.get("capacity")
        if capacity :
            capacity = int(capacity)
        else:
            capacity = 0
        projector = request.GET.get("projector") == "on"
        rooms = Room.objects.all().order_by("capacity")
        if projector:
            rooms = rooms.filter(projector_aval=projector)
        if capacity:
            rooms = rooms.filter(capacity__gte=capacity)
        if name:
            rooms = rooms.filter(name__contains=name)

        for room in rooms:
            reservation_dates = [reservation.date for reservation in room.reservation_set.all()]
            room.reserved = datetime.date.today() in reservation_dates

        return render(request, "room_search.html", context={"rooms": rooms})