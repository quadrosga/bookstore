import os
import git
import subprocess
import shutil
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update(request):
    print(f"Received {request.method} request at /upload_server/")

    if request.method == "POST":
        try:
            repo_path = "C:/Users/quadr/ebac/bookstore" if os.name == "nt" else "/home/quadrosga/bookstore"
            repo = git.Repo(repo_path)
            origin = repo.remotes.origin
            origin.pull()
            
            print("Successfully pulled latest code from GitHub.")

            # Reload the web app on PythonAnywhere
            if os.name != "nt":  # Only run this on Linux/PythonAnywhere
                touch_cmd = shutil.which("touch")
                if touch_cmd:
                    subprocess.run([touch_cmd, "/var/www/quadrosga_pythonanywhere_com_wsgi.py"], check=True)
                    print("WSGI file touched to reload the app.")
                else:
                    print("Command 'touch' not found!")

            return HttpResponse("Updated code on PythonAnywhere")
        except Exception as e:
            print(f"Error updating: {e}")
            return HttpResponse(f"Error updating: {e}", status=500)

    print("Received non-POST request at /upload_server/")
    return HttpResponse("This endpoint only accepts POST requests.", status=405)

def hello_world(request):
    template = loader.get_template('hello_world.html')
    return HttpResponse(template.render())
