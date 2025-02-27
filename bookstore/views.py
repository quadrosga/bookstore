from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import git
from pathlib import Path

@csrf_exempt
def update(request):
    if request.method == "POST":
        try:
            repo = git.Repo('/home/quadrosga/bookstore')
            origin = repo.remotes.origin
            origin.pull()

            # Using pathlib instead of os.system("touch ...")
            wsgi_file = Path("/var/www/quadrosga_pythonanywhere_com_wsgi.py")
            wsgi_file.touch()

            return HttpResponse("Updated code on PythonAnywhere and reloaded server.")
        except Exception as e:
            return HttpResponse(f"Error updating: {str(e)}", status=500)
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere", status=400)

def hello_world(request):
    template = loader.get_template('hello_world.html')
    return HttpResponse(template.render())