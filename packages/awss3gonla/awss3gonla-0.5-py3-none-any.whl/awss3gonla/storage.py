from abc import ABC, abstractmethod
from typing import Union, Dict, Any

class IStorage(ABC):

    @abstractmethod
    def get(self,path,name):
        pass

    @abstractmethod
    def put(self,path:str,name:str):
        pass
    
    @abstractmethod
    def put_object(self,path:str,name:str,object:Union[str,Dict[str,Any]]):
        pass
    @abstractmethod
    def list(self,path:str):
        pass

        