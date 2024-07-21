'''
    Encoder
'''
import json
from datetime import datetime

class DateTimeEncoder(json.JSONEncoder):
    '''
        DateTime Encoder
    '''
    def default(self, obj):
        '''
            default
        '''
        if isinstance(obj, datetime):
            # Serialize datetime as an ISO 8601 string
            return obj.isoformat()

        return super().default(obj)
