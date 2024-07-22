import os


class BaseURLPatterns:
    def __init__(self, app_config, force):
        self.app_name = app_config.name
        self.url_patterns = []

    def generate_url_patterns(self, api_spec_path, app_urls, api_spec_file_name):
        app_path = os.path.abspath(self.app_name)
        app_urls_path = os.path.join(app_path, 'urls.py')
        file_path = api_spec_path.format(self.app_name)
        app_urls_template = app_urls.replace("{{app}}", self.app_name)
        app_urls_template = app_urls_template.replace("{{file_path}}", file_path)
        app_urls_template = app_urls_template.replace("{{API_SPEC_FILE_NAME}}", api_spec_file_name)
        with open(app_urls_path, 'w') as file:
            file.write(app_urls_template)


class URLPatternsGenerator(BaseURLPatterns):
    def __init__(self, app_config, force):
        super(URLPatternsGenerator, self).__init__(app_config, force)
        