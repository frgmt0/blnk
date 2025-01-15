from abc import ABC, abstractmethod

class BaseAPI(ABC):
    @abstractmethod
    async def send_message(self, message):
        pass

    @abstractmethod
    def get_name(self):
        pass
        
    @abstractmethod
    def get_available_models(self):
        pass
        
    @abstractmethod
    def set_model(self, model_name):
        pass
