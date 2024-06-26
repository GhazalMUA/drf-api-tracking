from .base_mixins import BaseLoggingMixin
from .models import APIRequestLog

class LoggingMixin(BaseLoggingMixin):
    def handle_log(self):
        APIRequestLog(**self.log).save()        # indota setare yani in dictionry i ke tooye self.log hastesh ro baz kon vasamoon.
        print(self.log)
        
        
        