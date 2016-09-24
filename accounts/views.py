from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.forms import SignUpForm


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {
        "form": form
    })



# <form method="POST" action="{% block form_action %}{% endblock %}">
#     {{ form.text }}
#     {% csrf_token %}
#     {% if form.errors %}
#         <div class="form-group has-error">
#             <div class="help-block">{{ form.text.errors }}</div>
#         </div>
#     {% endif %}
# </form>


# {% for field in form %}
#     <div class="fieldWrapper">
#         {{ field.errors }}
#         {{ field.label_tag }} {{ field }}
#         {% if field.help_text %}
#         <p class="help">{{ field.help_text|safe }}</p>
#         {% endif %}
#     </div>
# {% endfor %}