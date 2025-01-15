from abc import ABC, abstractmethod                                                                            
                                                                                                            
class BaseAPI(ABC):                                                                                            
    @abstractmethod                                                                                            
    def send_message(self, message):                                                                           
        pass                                                                                                   
                                                                                                            
    @abstractmethod                                                                                            
    def get_name(self):                                                                                        
        pass  