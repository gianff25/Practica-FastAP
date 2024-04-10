from sqlalchemy_mixins.utils import classproperty


class ExceptionContext:
    _exceptions = []

    @classmethod
    def add_exception(cls, exception):
        cls._exceptions.append(exception)

    @classmethod
    def set_exceptions(cls, exceptions):
        """
        :type exception: exception | Exception
        """
        cls._exceptions = exceptions

    @classproperty
    def exceptions(cls):
        """
        :rtype: exception | Exception
        """
        return cls._exceptions
