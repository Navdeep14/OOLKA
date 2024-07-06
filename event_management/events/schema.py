# myapp/schema.py

from rest_framework.schemas.openapi import AutoSchema

class CustomSchema(AutoSchema):
    def get_operation(self, path, method):
        operation = super().get_operation(path, method)
        
        # Add custom tags
        operation['tags'] = ['custom_tag']

        # Add custom metadata
        operation['description'] = 'This is a custom description'
        operation['summary'] = 'Custom summary for the endpoint'

        # Example of adding a custom response
        operation['responses']['400'] = {
            'description': 'Bad Request',
            'content': {
                'application/json': {
                    'example': {
                        'error': 'Bad Request',
                        'message': 'Invalid input provided'
                    }
                }
            }
        }

        return operation
