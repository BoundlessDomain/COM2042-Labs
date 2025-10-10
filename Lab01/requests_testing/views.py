from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
# # This is a method called "hello_world" which takes a single parameter called "request".
# def hello_world(request):
#     # This gets a "message" parameter. If it is not there, defaults to "Hello world!".
#     message_text = request.GET.get('message', 'Hello world!')
#     # The "HttpResponse" class returns the message "Hello world!".
#     return HttpResponse(message_text)

def hello_world(request):
    # Checks for custom headers.
    header_message = request.headers.get('MY-APPLICATION-MESSAGE')

    if header_message:
        message_text = header_message
    else:
        # If there is no header, check for the GET parameter.
        message_text = request.GET.get('message', 'Hello world!')

    return HttpResponse(message_text)
