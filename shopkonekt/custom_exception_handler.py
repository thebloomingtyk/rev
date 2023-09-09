# from rest_framework.views import exception_handler
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.exceptions import ValidationError


# def custom_exception_handler(exc, context):
#     # Use the default exception handler for non-ValidationError exceptions
#     response = exception_handler(exc, context)

#     if isinstance(exc, ValidationError):
#         # Custom error response format for ValidationError
#         error_message = list(exc.detail.values())[0][0]
#         response_data = {'error': error_message}
#         response = Response(response_data, status=status.HTTP_400_BAD_REQUEST)

#     return response


from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

def custom_exception_handler(exc, context):
    # Use the default exception handler for non-ValidationError exceptions
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError):
        # Check if the 'detail' dictionary contains any items
        if 'detail' in exc.detail:
            # Check if the first item in 'detail' has any errors
            if exc.detail['detail']:
                error_message = list(exc.detail['detail'])[0]
                response_data = {'error': error_message}
                response = Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    return response
