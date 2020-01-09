import json
from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from todolist import constants
from todolist.models import Event, EventClass
from todolist.forms import TodoUserForm


@csrf_exempt
def todo_login(request):
    """
    If this is a POST request, try to login
    with the given username and password
    Otherwise, return the login page
    """
    error_info = ""
    if request.POST:
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("todo_main"))
        error_info = constants.NAME_PASSWORD_DOESNT_MATCH_MSG
    logout(request)
    return render_to_response(
        "todo_login.html", {"error_info": error_info,}, RequestContext(request)
    )


@csrf_exempt
def todo_reg(request):
    """
    If this is a POST request, try to register
    the user with the given user information
    Otherwise, return the register page
    """
    error_info = ""
    if request.POST:
        todo_user_form = TodoUserForm(request.POST)
        if todo_user_form.is_valid():
            new_user = todo_user_form.save()
            # Create the 'Default' Class for the new user
            EventClass.objects.create(name="Default", order="0", user=new_user)
            new_user = authenticate(
                username=request.POST["username"], password=request.POST["password1"]
            )
            login(request, new_user)
            return HttpResponseRedirect(reverse("todo_main"))
        error_info = todo_user_form.errors
    return render_to_response(
        "todo_reg.html", {"error_info": error_info,}, RequestContext(request)
    )


@csrf_exempt
def get_event_classes(request):
    """
    Get the classes of the given user id
    """
    if request.user.is_authenticated:
        response = dict()
        response["data"] = [
            {"id": x.id, "name": x.name}
            for x in EventClass.get_classes_by_user(request.user.id).order_by("order")
        ]
        return HttpResponse(json.dumps(response), content_type="application/json")
    return render_to_response(
        "todo_login.html",
        {"error_info": constants.SESSION_EXPIRED_MSG,},
        RequestContext(request),
    )


@csrf_exempt
def add_event_class(request):
    """
    Add a new event class to the given user
    """
    if request.user.is_authenticated:
        new_event_class_dict = {
            "user": request.user,
            "name": request.POST.get("className", None),
            "order": request.POST.get("order", None),
        }
        new_event_class = EventClass.objects.create(**new_event_class_dict)
        response = dict()
        response["data"] = new_event_class.id
        return HttpResponse(json.dumps(response), content_type="application/json")
    return render_to_response(
        "todo_login.html",
        {"error_info": constants.SESSION_EXPIRED_MSG,},
        RequestContext(request),
    )


@csrf_exempt
def update_event_classes_order(request):
    """
    Update the order of the event classes of the
    given user. There should be a dictionary in the request
    containing id and order or each event class
    """
    if request.user.is_authenticated:
        for event_class_id in request.POST:
            EventClass.get_classes_by_user(request.user.id).filter(
                id=event_class_id
            ).update(order=request.POST[event_class_id])
        return HttpResponse(json.dumps({}), content_type="application/json")
    return render_to_response(
        "todo_login.html",
        {"error_info": constants.SESSION_EXPIRED_MSG,},
        RequestContext(request),
    )


@csrf_exempt
def remove_event_class(request):
    """
    Remove the given event class, and update the
    order of the rest classes
    """
    if request.user.is_authenticated:
        class_id = request.POST.get("classId", None)
        event_class = EventClass.get_classes_by_user(request.user.id).get(id=class_id)
        event_class.delete()
        return HttpResponse(json.dumps({}), content_type="application/json")
    return render_to_response(
        "todo_login.html",
        {"error_info": constants.SESSION_EXPIRED_MSG,},
        RequestContext(request),
    )


@csrf_exempt
def get_event(request):
    """
    Get the events of the given class id
    """
    if request.user.is_authenticated:
        response = {}
        class_id = request.GET.get("classId", None)
        done = request.GET.get("done", None)
        if done == "1":
            response["data"] = Event.get_events_dict_by_class(class_id, True)[
                : constants.DONE_EVENTS_LIMIT
            ]
        else:
            response["data"] = Event.get_events_dict_by_class(class_id, False)
        return HttpResponse(json.dumps(response), content_type="application/json")
    return render_to_response(
        "todo_login.html",
        {"error_info": constants.SESSION_EXPIRED_MSG,},
        RequestContext(request),
    )


@csrf_exempt
def add_event(request):
    """
    Add a new event to the given user
    """
    if request.user.is_authenticated:
        event_class = EventClass.objects.get(id=request.POST.get("classId", None))
        new_event_dict = {
            "eventclass": event_class,
            "content": request.POST.get("content", None),
            "priority": 0,
            "done": 0,
            "order": request.POST.get("order", None),
            "duedate": request.POST.get("dueDate", None),
        }
        new_event = Event.objects.create(**new_event_dict)
        response = dict()
        response["data"] = new_event.id
        return HttpResponse(json.dumps(response), content_type="application/json")
    return render_to_response(
        "todo_login.html",
        {"error_info": constants.SESSION_EXPIRED_MSG,},
        RequestContext(request),
    )


@csrf_exempt
def update_event(request):
    """
    Update the event, possible activities are:
    1. Text edit
    2. Check the event
    3. Priority edit
    """
    if request.user.is_authenticated:
        update_type = request.POST.get("type", None)
        event_id = request.POST.get("eventId", None)
        if update_type == "text":
            Event.objects.filter(id=event_id).update(content=request.POST["content"])
        elif update_type == "check":
            Event.objects.filter(id=event_id).update(done=True, duedate=date.today())
        elif update_type == "priority":
            Event.objects.filter(id=event_id).update(priority=request.POST["priority"])
        return HttpResponse(json.dumps({}), content_type="application/json")
    return render_to_response(
        "todo_login.html",
        {"error_info": constants.SESSION_EXPIRED_MSG,},
        RequestContext(request),
    )


@csrf_exempt
def update_events_order(request):
    """
    Update the order of the events of the
    given user. There should be a dictionary in the request
    containing id and order or each event
    """
    if request.user.is_authenticated:
        class_id = request.POST.get("classId", None)
        for event_id in request.POST:
            Event.objects.filter(id=event_id).update(order=request.POST[event_id])
        return HttpResponse(json.dumps({}), content_type="application/json")
    return render_to_response(
        "todo_login.html",
        {"error_info": constants.SESSION_EXPIRED_MSG,},
        RequestContext(request),
    )


@csrf_exempt
def remove_event(request):
    """
    Remove the given event, and update the
    order of the rest events
    """
    if request.user.is_authenticated:
        event_id = request.POST.get("eventId", None)
        event = Event.objects.get(id=event_id)
        event.delete()
        return HttpResponse(json.dumps({}), content_type="application/json")
    return render_to_response(
        "todo_login.html",
        {"error_info": constants.SESSION_EXPIRED_MSG,},
        RequestContext(request),
    )
