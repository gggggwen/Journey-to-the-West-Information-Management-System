from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "home.html")

def main_page(request):
    return render(request, "main_page.html")