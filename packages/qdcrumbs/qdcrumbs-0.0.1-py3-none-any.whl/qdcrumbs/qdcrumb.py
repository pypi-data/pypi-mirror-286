from flask import url_for
from inspect import stack, getmodule
from .breadcrumb import Breadcrumb
import os.path

class QDCrumbs:
    def __init__(self, app_name:str = 'app'):
        self.app_name = app_name

    #Redefine the app's name if not naped "app", this should be the 
    # same as __name__ in app = Flask(__name__)
    # If the application is named app, there is no need to use this
    def set_app_name(self, app_name):
        self.app_name = app_name
    
    def get_crumbs(self, page: str = None):

        #Gets the calling function's & filename (in case of blueprints)
        # to use as parameter for url_for()
        frame = stack()[1]
        module = getmodule(frame[0])
        file_path = module.__file__
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        if file_name == self.app_name:
            calling_function = frame.function
        else:
            calling_function = file_name + "." + frame.function
        
        #Get the route to the resource 
        # (works with a single variable page)
        full_url = url_for(calling_function, page=page)

        #Strip and split the url
        components = full_url.strip('/').split('/')
        
        #Make a list of all found breadcrumbs (forwards)
        crumbs = []
        for i in range(len(components),-1,-1):
            if components:
                crumb = '/' + '/'.join(components[:i])
                text = components.pop()
                print(text)
                tmp = Breadcrumb(crumb, text)
                crumbs.append(tmp)
        
        #Reverse the breadcrumb order (to make using in jinja2 easier)
        crumbs.reverse()
        
        return crumbs
