from django.shortcuts import render


def home_page(request):
    # Start with popular browsing mode
    request.session["browse_mode"] = "popular"
    request.session["browse_page"] = 1

    return render(request, "main/home.html")

