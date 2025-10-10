from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def hello_world(request): #This is a method called "hello_world" which takes a single parameter called "request".
    message_text = request.GET.get('message', 'Hello world!') #This gets a "message" parameter. If it is not there, defaults to "Hello world!".
    return HttpResponse("Hello world!") #The "HttpResponse" class returns the message "Hello world!".