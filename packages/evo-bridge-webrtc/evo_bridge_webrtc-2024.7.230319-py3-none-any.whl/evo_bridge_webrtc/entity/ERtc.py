#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation    https://github.com/cyborg-ai-git | 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

#========================================================================================================================================
"""ERtc

    ERtc _DOC_
    
"""
class ERtc(EObject):

    VERSION:str="a06006e195466f4fc97248eb8e03f4ac366079156b9a3b768a893563f884dfaf"

    def __init__(self):
        super().__init__()
        
        self.offerID:str = None
        self.answerID:str = None
        self.sdpOffer:str = None
        self.sdpAnswer:str = None
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteStr(self.offerID, stream)
        self._doWriteStr(self.answerID, stream)
        self._doWriteStr(self.sdpOffer, stream)
        self._doWriteStr(self.sdpAnswer, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.offerID = self._doReadStr(stream)
        self.answerID = self._doReadStr(stream)
        self.sdpOffer = self._doReadStr(stream)
        self.sdpAnswer = self._doReadStr(stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\tofferID:{self.offerID}",
                f"\tanswerID:{self.answerID}",
                f"\tsdpOffer:{self.sdpOffer}",
                f"\tsdpAnswer:{self.sdpAnswer}",
                            ]) 
        return strReturn
    