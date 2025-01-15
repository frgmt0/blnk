from .base_api import BaseAPI                                                                                  
                                                                                                            
class EchoAPI(BaseAPI):
    def __init__(self):
        super().__init__()  # Initialize BaseAPI
                                                                                        
    async def send_message(self, message):                                                                           
        return f"Echo: {message}"                                                                              
                                                                                                            
    def get_name(self):                                                                                        
        return "echo" 
