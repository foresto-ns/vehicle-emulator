from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.inspectors import SwaggerAutoSchema


class CustomAutoSchema(SwaggerAutoSchema):
    """Схема описания работы сваггера"""
    def get_tags(self, operation_keys=None):
        tags = self.overrides.get('tags', None) or getattr(self.view, 'swagger_tags', [])
        if not tags:
            tags = [operation_keys[0]]

        return tags


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    """Схема описания работы сваггера"""
    def get_schema(self, request=None, public=False):
        """Generate a :class:`.Swagger` object with custom tags"""
        swagger = super().get_schema(request, public)
        return swagger
