from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

import git
import os


@csrf_exempt
def update(request):
    if request.method == "POST":
        try:
            repo = git.Repo('/home/quadrosga/bookstore')
            origin = repo.remotes.origin
            pull_info = origin.pull()
            
            # Debugging: Log what was pulled
            pulled_commits = [commit.hexsha for commit in pull_info]
            log_message = f"Pulled commits: {pulled_commits}"

            # Force reload on PythonAnywhere
            import os
            os.system("touch /var/www/quadrosga_pythonanywhere_com_wsgi.py")

            return HttpResponse(f"Updated code on PythonAnywhere. {log_message}")
        except Exception as e:
            return HttpResponse(f"Error updating: {str(e)}", status=500)
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere", status=400)