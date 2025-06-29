from fastapi.templating import Jinja2Templates

class BrowserViewHandler:
    def __init__(self, jinja2_templates):
        self.templates: Jinja2Templates = jinja2_templates


    def get_html_response(self, request, user):
        context = {}
        return self.templates.TemplateResponse(request, 'browser.html', context)