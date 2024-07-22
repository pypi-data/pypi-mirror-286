import json
import shutil
import os
import time
import logging
from pathlib import Path
from django.template import Template
from django_swagger_utils.server.templates.app_urls import APP_URLS
from django_swagger_utils.server.templates.views import VIEWS_TEMPLATE
from django_swagger_utils.server.templates.apiview import API_VIEW_TEMPLATE
from django_swagger_utils.server.templates.validator_class import VALIDATOR_CLASS
from django_swagger_utils.server.templates.api_wrapper import API_WRAPPER_TEMPLATE
from django_swagger_utils.server.constants.paths import API_SPEC_PATH, VIEWS_ABS_PATH, API_SPEC_FILE_NAME
from django_swagger_utils.server.generators.url_generator import URLPatternsGenerator
from django_swagger_utils.server.templates.request_response_mocks import REQUEST_RESPONSE_MOCKS
from django_swagger_utils.server.templates.modelviewset import MODEL_URL_TEMPLATE, MODEL_VIEW_TEMPLATE
from django_swagger_utils.server.constants.paths import VIEWS_ABS_PATH, INIT_FILE_NAME, TESTS_DIRECTORY_NAME, \
    API_SPEC_OPERATION_ID, API_SPEC_RESPONSES
from django_swagger_utils.server.exceptions.view_generator_exceptions import OVERWRITE_FILENAME, CLEANUP_COMPLETED, \
    CLEANUP_FAILED, VIEWS_GENERATION_FAILED
from django_swagger_utils.server.constants.view_structure import VIEW_STRUCTURE, API_WRAPPER_FILE, \
    REQUEST_RESPONSE_MOCKS_FILE, VALIDATOR_CLASS_FILE

__all__ = ['BaseGenerator', 'APIViewGenerator', 'ViewSetGenerator',
           'FunctionViewGenerator', 'ModelViewSetGenerator']


class BaseGenerator(object):

    def __init__(self, app_config, force):
        self.app_config = app_config
        self.force = force
        self.name = app_config.name
        self.logger = logging.getLogger(__name__)
        self.overwrite_all = False  # Flag to track user's decision to overwrite all files
        self.overwrite_none = False  # Flag to track user's decision to not overwrite any files

    @staticmethod
    def create_init_file(directory, content=''):
        with open(os.path.join(directory, INIT_FILE_NAME), 'w') as file:
            file.write(content)

    def generate_views(self, url_paths):
        views_path = VIEWS_ABS_PATH.format(os.path.abspath(self.name))
        
        # Check if files already exist and prompt user accordingly
        existing_directories = []
        new_directories = {}
        url_path_items = [(k, v) for k, v in url_paths.items()]
        if not self.check_and_prompt_overwrite(existing_directories):
            self.logger.info("User chose not to overwrite existing directories. Skipping file generation.")
        else:
            self.overwrite_all = True
            
        for item in url_paths.items():
            for http_method, operation_details in url_paths[item[0]].items():
                views_path = VIEWS_ABS_PATH.format(os.path.abspath(self.name))
                operation_id = operation_details.get(API_SPEC_OPERATION_ID)
                views_directory_path = os.path.join(views_path, operation_id)
                tests_directory_path = os.path.join(views_path, operation_id)
                if os.path.exists(views_directory_path):
                    if self.overwrite_all:
                        # if self.cleanup_generated_files(views_directory_path):
                        self.create_python_directory(views_directory_path)
                        self.create_python_directory(tests_directory_path)
                        self.generate_views_required_files(views_directory_path, operation_details.get(API_SPEC_RESPONSES), operation_id)
                    else:
                        continue
                else:
                    self.create_python_directory(views_directory_path)
                    self.create_python_directory(tests_directory_path)
                    self.generate_views_required_files(views_directory_path, operation_details.get(API_SPEC_RESPONSES), operation_id)
                        

    
    def write_file(self, content, filename, directory):
        try:
            name = os.path.join(directory, filename)
            if os.path.exists(name) and not self.force and not self.overwrite_all:
                if self.overwrite_none:
                    return False
                msg = OVERWRITE_FILENAME % filename
                response = input(f"{msg} (y/n/a): ")
                if response == "n":
                    return False
                elif response == "a":
                    self.overwrite_all = True
                elif response == "n":
                    self.overwrite_none = True
                    return False
            with open(name, 'w') as file:
                file.write(content)
            return True
        except Exception as e:
            self.logger.error(f"Error writing file {filename}: {str(e)}")
            return False

    def check_and_prompt_overwrite(self, existing_files):
        """Prompt user for overwrite confirmation."""
        msg = "Files already exist in the views directory:\n"
        for file in existing_files:
            msg += f"- {file}\n"
        msg += "Overwrite all existing files? (y/n): "
        response = input(msg)
        if response == "y":
            self.overwrite_all = True
            return True
        elif response == "n":
            self.overwrite_none = True
            return False
        return True

    def check_existing_files(self, views_path):
        """Check for existing files in the views path."""
        existing_files = list(Path(views_path).rglob('*'))
        return existing_files

    def generate_views_required_files(self, view_path, responses, operationId):
        for key, value in VIEW_STRUCTURE.items():
            view_directory = os.path.join(view_path, value)
            try:
                if value == API_WRAPPER_FILE:
                    self.generate_api_wrapper(view_path, value, operationId)
                elif value == REQUEST_RESPONSE_MOCKS_FILE:
                    self.generate_request_response_mocks(view_path, value, responses)
                elif value == VALIDATOR_CLASS_FILE:
                    self.generate_validator_class(view_path, value)
            except Exception as e:
                self.logger.error(f"Error generating views required files: {str(e)}")
                return False
        self.generate_view_function("{}.py".format(operationId), view_path, operationId)
        return True

    def generate_view_function(self, file, view_directory, operationId):
        return self.write_file(VIEWS_TEMPLATE.replace("{{operation_id}}", operationId), file, view_directory)
    
    def generate_api_wrapper(self, view_directory, file, operation_id):
        return self.write_file(API_WRAPPER_TEMPLATE, file, view_directory)
    
    def generate_request_response_mocks(self, view_directory, file, responses):
        request_response_content = REQUEST_RESPONSE_MOCKS.replace("{{request_response}}", json.dumps(responses))
        return self.write_file(request_response_content, file, view_directory)
    
    def generate_validator_class(self, view_directory, file):
        return self.write_file(VALIDATOR_CLASS, file, view_directory)
    
    def create_python_directory(self, directory_path, content='', force=True):
        try:
            if force and os.path.exists(directory_path):
                shutil.rmtree(directory_path)
            if not os.path.exists(directory_path):
                os.mkdir(directory_path)
                self.create_init_file(directory_path, content)
        except Exception as e:
            self.logger.error(f"Error creating directory {directory_path}: {str(e)}")
    
    def cleanup_generated_files(self, directory_path):
        print("cleaning up generated files...")
        try:
            if os.path.exists(directory_path):
                print("Path Exists: ", directory_path)
                shutil.rmtree(directory_path)
                self.logger.info(CLEANUP_COMPLETED.format(directory_path))
                return True
        except Exception as e:
            self.logger.error(CLEANUP_FAILED.format(str(e)))
            return False

    def generate_app_urls(self, url_paths):
        generate_url_patterns_instance = URLPatternsGenerator(self.app_config, force=False)
        try:
            generate_url_patterns_instance.generate_url_patterns(API_SPEC_PATH, APP_URLS, API_SPEC_FILE_NAME)
        except Exception as e:
            self.logger.error(VIEWS_GENERATION_FAILED.format(str(e)))


class APIViewGenerator(BaseGenerator):

    def __init__(self, app_config, force):
        super(APIViewGenerator, self).__init__(app_config, force)
        self.view_template = Template(API_VIEW_TEMPLATE)


class ViewSetGenerator(BaseGenerator):

    def __init__(self, app_config, force):
        super(ViewSetGenerator, self).__init__(app_config, force)


class FunctionViewGenerator(BaseGenerator):

    def __init__(self, app_config, force):
        super(FunctionViewGenerator, self).__init__(app_config, force)


class ModelViewSetGenerator(BaseGenerator):

    def __init__(self, app_config, force):
        super(ModelViewSetGenerator, self).__init__(app_config, force)
        self.view_template = Template(MODEL_VIEW_TEMPLATE)
        self.url_template = Template(MODEL_URL_TEMPLATE)