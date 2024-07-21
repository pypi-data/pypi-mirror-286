import sys as system
import os
import json
import re
from .__init__ import MAIN_PATH
from .type_validation import *

HOST_DICT = {
    "host": {"type": str},
    "cert_path" : {"type": str},
	"key_path" : {"type": str}
}

HOST_SCHEME = Union[str, List[Scheme[HOST_DICT]]]

class Config:
    def __init__(self) -> None:
        
        '''The config class loads the config attributes form the config.json file
        if an error occurs the programm will terminate.'''
        
        config_path = MAIN_PATH +"/config/config.json"
        
        self.HOST = None
        self.MAX_THREADS = 50
        
        with open(config_path,'r') as file:
            error_prefix = '[CONFIG_ERROR]'
            content = ''.join(file.readlines())
            config = json.loads(content)
            if 'ip' in config:
                self.SERVER_IP = config['ip']
            else:
                print(error_prefix," the required property 'ip' is missing.")
                system.exit(0)
            if 'port' in config:
                self.SERVER_PORT = config['port']
            else:
                print(error_prefix," the required property 'port' is missing.")
                system.exit(0)
            if 'queue_size' in config:
                self.QUE_SIZE = config['queue_size']
            else:
                print(error_prefix," the required property 'queue_size' is missing.")
                system.exit(0)
            if 'max_threads' in config:
                self.MAX_THREADS = config['max_threads']
            else:
                print(error_prefix," the property 'max_threads' is missing.")
                self.MAX_THREADS = 10
            if 'SSL' in config:
                self.SSL = config['SSL']
            else:
                print(error_prefix," the required property 'SSL' is missing.")
                system.exit(0)
            if self.SSL:
                if 'host' in config:
                    if not satisfies(config['host'], HOST_SCHEME, True):
                        system.exit(0)
                    self.HOST = config['host']
                else:
                    print(error_prefix,"Use the 'host' field to support SNI.")
                if 'cert_path' in config:
                    self.CERT_PATH = config['cert_path']
                else:
                    print(error_prefix," the required property 'cert_path' is missing.")
                    system.exit(0)
                if 'key_path' in config:
                    self.KEY_PATH = config['key_path']
                else:
                    print(error_prefix," the required property 'key_path' is missing.")
                    system.exit(0)
                
           
