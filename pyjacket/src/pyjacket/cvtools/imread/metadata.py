from typing import Protocol

@Protocol
class Metadata:
            
    @property        
    def exposure_time(self):
        """Camera exposure time in ms"""
    
    @property
    def light_intensity(self):
        """Light intensity in percentage"""