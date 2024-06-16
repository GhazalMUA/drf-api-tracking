

class BaseLoggingMixin:
    def initial(self, request, *args, **kwargs):
        print('*' * 100)
        print('initial method')
        return super().initial(request, *args, **kwargs)
    
    def finalize_response(self, request, response, *args, **kwargs):
        print('*' * 100)
        print('finalize method')
        return super().finalize_response(request, response, *args, **kwargs)
    
    