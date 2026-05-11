import datetime
import logging

class AccessGatewayFilter:
    """
    This class is a filter used for accessing gateway filtering, primarily for authentication and access log recording.
    """

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("AccessGatewayFilter")
        self.current_user = None

    def filter(self, request):
        """
        Filter the incoming request based on certain rules and conditions.
        :param request: dict, the incoming request details
        :return: bool, True if the request is allowed, False otherwise
        """
        path = request.get('path', '')
        
        if self.is_start_with(path):
            return True
        
        user = self.get_jwt_user(request)
        if user:
            self.set_current_user_info_and_log(user)
            return True
            
        return False

    def is_start_with(self, request_uri):
        """
        Check if the request URI starts with certain prefixes.
        Currently, the prefixes being checked are "/api" and "/login".
        :param request_uri: str, the URI of the request
        :return: bool, True if the URI starts with certain prefixes, False otherwise
        """
        allowed_prefixes = ('/api', '/login')
        return request_uri.startswith(allowed_prefixes)

    def get_jwt_user(self, request):
        """
        Get the user information from the JWT token in the request.
        :param request: dict, the incoming request details
        :return: dict or None, the user information if the token is valid, None otherwise
        """
        headers = request.get('headers', {})
        auth = headers.get('Authorization')
        
        if auth and 'jwt' in auth:
            expected_jwt = auth.get('user', {}).get('name', '') + str(datetime.date.today())
            if auth['jwt'] == expected_jwt:
                return auth.get('user')
        return None

    def set_current_user_info_and_log(self, user):
        """
        Set the current user information and log the access.
        :param user: dict, the user information
        :return: None
        """
        self.current_user = user
        self.logger.info(f"Access granted for user: {user.get('name', 'unknown')}")