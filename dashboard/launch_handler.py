from .handler import HTTPHandler


class LauncherHandler(HTTPHandler):
    def initialize(self, template=None, template_kwargs=None, **kwargs):
        super(LauncherHandler, self).initialize()
        self.template = template
        self.template_kwargs = template_kwargs or {}

    def get(self, *args):
        '''Get the login page'''
        if not self.template:
            self.redirect('/')
        else:
            if self.request.path == '/logout':
                self.clear_cookie("user")
            template = self.render_template(self.template, **self.template_kwargs)
            self.write(template)
