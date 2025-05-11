import sys
from networksecurity.logging import logger
class NetworkSecurityException(Exception):
    def __init__(self,error_msg,error_details:sys):
        self.error_msg = error_msg
        _,_,exc_tb=error_details.exc_info()
        
        self.lineno=exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename
    def __str__(self):#overriding the functionality
        return f"Error encountered in the code [{0}] at line [{1}]  Error: [{2}]".format(
        self.file_name, self.lineno, str(self.error_msg)
    )

