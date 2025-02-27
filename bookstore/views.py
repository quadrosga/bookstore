import logging
import os
import git
import subprocess
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

# Set up logging:
log_file = "C:/Users/quadr/ebac/bookstore/update_server.log" if os.name == "nt" else "/tmp/update_server.log"

logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)  # <-- Create logger instance

@csrf_exempt
def update(request):
    logger.debug(f"Received {request.method} request at /upload_server/")

    if request.method == "POST":
        try:
            repo_path = "C:/Users/quadr/ebac/bookstore" if os.name == "nt" else "/home/quadrosga/bookstore"
            repo = git.Repo(repo_path)
            origin = repo.remotes.origin
            origin.pull()
            
            logger.info("Successfully pulled latest code from GitHub.")

            # Reload the web app on PythonAnywhere
            if os.name != "nt":  # Only run this on Linux/PythonAnywhere
                subprocess.run(["touch", "/var/www/quadrosga_pythonanywhere_com_wsgi.py"], check=True)
                logger.info("WSGI file touched to reload the app.")

            return HttpResponse("Updated code on PythonAnywhere")
        except Exception as e:
            logger.error("Error updating repository", exc_info=True)
            return HttpResponse(f"Error updating: {e}", status=500)

    logger.warning("Received non-POST request at /upload_server/")
    return HttpResponse("This endpoint only accepts POST requests.", status=405)

def hello_world(request):
    template = loader.get_template('hello_world.html')
    return HttpResponse(template.render())
