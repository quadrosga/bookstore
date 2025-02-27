import os
import git
import subprocess
import shutil
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update(request):
    if request.path == "/favicon.ico":
        return HttpResponse(status=204)  # No Content (Silently ignore it)
    
    if request.method == "GET":
        return HttpResponse("<h1>This is the webhook update endpoint.</h1><p>Send a POST request to trigger an update.</p>")

    try:
        repo_path = "/home/quadrosga/bookstore" if os.name != "nt" else "C:/Users/quadr/ebac/bookstore"
        repo = git.Repo(repo_path)
        origin = repo.remotes.origin
        origin.pull()
        
        if os.name != "nt":
            with open("/var/www/quadrosga_pythonanywhere_com_wsgi.py", "a"):
                os.utime("/var/www/quadrosga_pythonanywhere_com_wsgi.py", None)

        return HttpResponse("Updated code on PythonAnywhere")
    except Exception as e:
        return HttpResponse(f"Error updating: {e}", status=500)

def hello_world(request):
    template = loader.get_template('hello_world.html')
    return HttpResponse(template.render())
