from django.shortcuts import render, redirect
from .models import Student
from .forms import StudentForm
from django.http import HttpResponse
import os
from django.conf import settings
from email_validator import validate_email, EmailNotValidError
from django.db.models import Q
import re
from django.template.loader import render_to_string


def index(request):
    students = Student.objects.all()
    if request.method == "POST":
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            id_number = form.cleaned_data.get("id_number")
            first_name = form.cleaned_data.get("first_name").capitalize()
            middle_initial = form.cleaned_data.get("middle_initial").upper()
            last_name = form.cleaned_data.get("last_name").capitalize()
            email_address = form.cleaned_data.get("email_address")
            gender = form.cleaned_data.get("gender")
            course_name = form.cleaned_data.get("course_name")
            year_level = form.cleaned_data.get("year_level")
            subjects = form.cleaned_data.get("subjects")
            image = form.cleaned_data.get("image")

            if Student.objects.filter(email_address=email_address).exists():
                error_message = "Email address already in use."
                return HttpResponse(error_message)

            # Validate image format
            image_extension = os.path.splitext(image.name)[1].lower()
            valid_image_formats = [".jpg", ".jpeg", ".png", ".gif"]

            filename = image.name
            image_path = os.path.join(settings.MEDIA_ROOT, "avatar", filename)
            with open(image_path, "wb") as f:
                for chunk in image.chunks():
                    f.write(chunk)

            student = Student(
                id_number=id_number,
                first_name=first_name,
                middle_initial=middle_initial,
                last_name=last_name,
                email_address=email_address,
                gender=gender,
                course_name=course_name,
                year_level=year_level,
                subjects=subjects,
                image=image_path,
            )

            if image_extension not in valid_image_formats:
                error_message = (
                    "Invalid image format. Only JPG, JPEG, PNG, or GIF are allowed."
                )
                return HttpResponse(error_message)

            if not re.match(pattern, email_address):
                error_message = "Invalid email address format"
                return HttpResponse(error_message)

            student.save()

            return redirect("/")
        else:
            error_messages = "\n".join(
                [
                    f"{field}: {', '.join(errors)}"
                    for field, errors in form.errors.items()
                ]
            )
            return HttpResponse(error_messages)
    else:
        return render(request, "index.html", {"students": students})


def search_students(request):
    search_query = request.GET.get("search", "")
    students = Student.objects.filter(
        Q(id_number__icontains=search_query)
        | Q(first_name__icontains=search_query)
        | Q(last_name__icontains=search_query)
    )

    # Render the table rows without the surrounding table structure
    html_content = render_to_string("students.html", {"students": students})
    return HttpResponse(html_content)
