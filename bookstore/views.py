from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import git
from pathlib import Path

import os
import git
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update(request):
    if request.method == "POST":
        # Detect environment (Windows vs. Linux/PythonAnywhere)
        if os.name == "nt":  # Windows
            repo_path = "C:/Users/quadr/ebac/bookstore"
        else:  # Linux (PythonAnywhere)
            repo_path = "/home/quadrosga/bookstore"

        try:
            repo = git.Repo(repo_path)
            origin = repo.remotes.origin
            origin.pull()
            return HttpResponse("Updated code on PythonAnywhere")
        except Exception as e:
            return HttpResponse(f"Error updating: {e}")
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere")

def hello_world(request):
    template = loader.get_template('hello_world.html')
    return HttpResponse(template.render())