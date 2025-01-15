from .base_api import BaseAPI                                                                                  
                                                                                                            
class EchoAPI(BaseAPI):                                                                                        
    def send_message(self, message):                                                                           
        return f"Echo: {message}"                                                                              
                                                                                                            
    def get_name(self):                                                                                        
        return "echo" 