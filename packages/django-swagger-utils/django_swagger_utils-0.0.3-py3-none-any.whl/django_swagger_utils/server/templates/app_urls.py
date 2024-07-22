APP_URLS = """import os
import json
import importlib
from django.urls import re_path

url_patterns = []

with open(os.path.join('{{file_path}}', '{{API_SPEC_FILE_NAME}}'), 'r') as file:
    content = file.read()
    swagger_data = json.loads(content)
    app_urls = swagger_data.get('paths')
    for url_path, operation_details in app_urls.items():
        for method, details in operation_details.items():
            if 'operationId' in details:
                operation_id = details.get('operationId')
                full_module_path = f'{{app}}.views.{operation_id}.{operation_id}'
                try:
                    module = importlib.import_module(full_module_path)
                    view_func = getattr(module, operation_id, None)
                    url_patterns.append(re_path(f'api/{{app}}{url_path}', view_func, name=operation_id))
                except ImportError as e:
                    print(f"Failed to import module '{full_module_path}': {e}")
"""
