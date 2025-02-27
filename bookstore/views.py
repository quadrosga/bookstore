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
    
    if request.method != "POST":
        print("Received non-POST request at /upload_server/")
        return HttpResponse("This endpoint only accepts POST requests.", status=405)

    try:
        repo_path = "/home/quadrosga/bookstore" if os.name != "nt" else "C:/Users/quadr/ebac/bookstore"
        repo = git.Repo(repo_path)
        origin = repo.remotes.origin
        origin.pull()
        
        if os.name != "nt":
            subprocess.run(["touch", "/var/www/quadrosga_pythonanywhere_com_wsgi.py"], check=True)

        return HttpResponse("Updated code on PythonAnywhere")
    except Exception as e:
        return HttpResponse(f"Error updating: {e}", status=500)

def hello_world(request):
    template = loader.get_template('hello_world.html')
    return HttpResponse(template.render())
