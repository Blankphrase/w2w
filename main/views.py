from django.shortcuts import render

def home_page(request):
    movies = [ index for index in range(10) ]
    return render(request, "main/home.html",
        {"movies": movies}
    )