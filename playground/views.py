from django.shortcuts import render

# Create your views here.
# request --> response
# request handler
# action :// some other frameworks
# in django it's a view


def calculate():
    x = 1
    y = 2
    return x


def say_hello(request):
    # pull data from db
    # transform
    # send email etc
    # return HttpResponse('Hello World!')
    calculate()
    return render(request, "hello.html")
