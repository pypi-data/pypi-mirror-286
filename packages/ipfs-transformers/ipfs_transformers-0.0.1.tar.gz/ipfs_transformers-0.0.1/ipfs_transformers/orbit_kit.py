import os
import sys
import subprocess as process 
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ipfs_transformers.orbit_kit import orbit_kit
class orbit_kit:
    def __init__(self, resources, meta=None):
        self.resources = resources
        self.meta = meta

    def start_orbitdb(self):
        start_orbitdb = process.Popen(['orbitdb', 'start'], stdout=process.PIPE, stderr=process.PIPE)
        pass

    def stop_orbitdb(self):
        stop_orbitdb = process.Popen(['orbitdb', 'stop'], stdout=process.PIPE, stderr=process.PIPE)
        pass
    
    def get_resources(self):
        return self.resources
    
if __name__ == '__main__':
    resources = {}
    meta = {}
    orbit_kit = orbit_kit(resources, meta)
    print(orbit_kit.get_resources())

