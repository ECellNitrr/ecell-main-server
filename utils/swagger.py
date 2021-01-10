from drf_yasg.openapi import Response
from rest_framework import serializers 

class PlaceholderSerialiser(serializers.Serializer):
    pass

# Used to create a example response object
def set_example(example, description='', schema=PlaceholderSerialiser):
    return Response(
        examples={"application/json": example},
        description=description, 
        schema=schema
    )