from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

import git
import os


@csrf_exempt
def update(request):
    if request.method == "POST":
        '''
        pass the path of the diectory where your project will be
        stored on PythonAnywhere in the git.Repo() as parameter.
        Here the name of my directory is "test.pythonanywhere.com"
        '''
        repo = git.Repo('/home/quadrosga/bookstore')
        origin = repo.remotes.origin

        origin.pull()
        return HttpResponse("Updated code on PythonAnywhere")
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere")
    
os.system("touch /var/www/quadrosga_pythonanywhere_com_wsgi.py")


def hello_world(request):
  template = loader.get_template('hello_world.html')
  return HttpResponse(template.render())

