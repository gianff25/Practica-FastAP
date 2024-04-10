from sqlalchemy_mixins.utils import classproperty


class RequestContext:
    _request = None

    @classmethod
    def set_request(cls, request):
        """
        :type request: request | Request
        """
        cls._request = request

    @classproperty
    def request(cls):
        """
        :rtype: request | Request
        """
        return cls._request
