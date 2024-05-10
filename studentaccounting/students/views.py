from django.shortcuts import render, redirect
from .models import Student
from .forms import StudentForm
from django.http import HttpResponse
import os
from django.conf import settings


def index(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            id_number = form.cleaned_data.get("id_number")
            first_name = form.cleaned_data.get("first_name")
            middle_initial = form.cleaned_data.get("middle_initial")
            last_name = form.cleaned_data.get("last_name")
            email_address = form.cleaned_data.get("email_address")
            gender = form.cleaned_data.get("gender")
            course_name = form.cleaned_data.get("course_name")
            year_level = form.cleaned_data.get("year_level")
            subjects = form.cleaned_data.get("subjects")
            image = form.cleaned_data.get("image")

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

            filename = image.name
            # Set the path where you want to save the image
            image_path = os.path.join(settings.MEDIA_ROOT, "avatar", filename)
            # Save the image to the specified path
            with open(image_path, "wb") as f:
                for chunk in image.chunks():
                    f.write(chunk)

            student.save()
            # Correctly returning HttpResponse
            return redirect("/")
        else:
            error_messages = "\n".join(
                [
                    f"{field}: {', '.join(errors)}"
                    for field, errors in form.errors.items()
                ]
            )
            # Correctly returning HttpResponse
            return HttpResponse(f"{error_messages}")
    else:
        students = Student.objects.all()
        return render(request, "index.html", {"students": students})
