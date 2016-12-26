from django.shortcuts import render

def main_interface(req):
    return render(req, "main.html")
