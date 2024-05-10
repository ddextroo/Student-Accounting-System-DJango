from django.shortcuts import render, redirect
from .models import Student
from .forms import StudentForm
from django.http import HttpResponse
import os
from django.conf import settings
from email_validator import validate_email, EmailNotValidError


def index(request):
    if request.method == "POST":
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

            # Validate image format
            image_extension = os.path.splitext(image.name)[1].lower()
            valid_image_formats = [".jpg", ".jpeg", ".png", ".gif"]
            if image_extension not in valid_image_formats:
                return render(
                    request,
                    "index.html",
                    {
                        "students": students,
                        "error_messages": "Invalid image format. Only JPG, JPEG, PNG, or GIF are allowed.",
                    },
                )
            try:
                v = validate_email(email_address)
                email_address = v["email"]
            except EmailNotValidError as e:
                return render(
                    request,
                    "index.html",
                    {
                        "students": students,
                        "error_messages": str(e),
                    },
                )

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
                image=image,
            )
            student.save()

            filename = image.name
            image_path = os.path.join(settings.MEDIA_ROOT, "avatar", filename)
            with open(image_path, "wb") as f:
                for chunk in image.chunks():
                    f.write(chunk)

            return redirect("/")
        else:
            error_messages = "\n".join(
                [
                    f"{field}: {', '.join(errors)}"
                    for field, errors in form.errors.items()
                ]
            )
            students = Student.objects.all()
            return render(
                request,
                "index.html",
                {"students": students, "error_messages": error_messages},
            )
    else:
        students = Student.objects.all()
        return render(request, "index.html", {"students": students})
