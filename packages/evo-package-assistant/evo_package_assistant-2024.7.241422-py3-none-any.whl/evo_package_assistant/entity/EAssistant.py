
#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation    https://github.com/cyborg-ai-git | 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_package_assistant.entity.EAssistantMessage import EAssistantMessage
from evo_package_assistant.entity.EAssistantTool import EAssistantTool

#<
from evo_framework.core.evo_core_crypto.utility.IuCryptHash import IuCryptHash
from evo_package_assistant.entity.EnumAssistantRole import EnumAssistantRole
from evo_framework.core.evo_core_api.entity import *
#>

#========================================================================================================================================
"""EAssistant

    EAssistant DESCRIPTION
    
"""
class EAssistant(EObject):

    VERSION:str="1ca1bac23a53b816a27b8d7f882f00027c03f99457e9051c27a56dc894b3c006"

    def __init__(self):
        super().__init__()
        
        self.name:str = None
        self.systemID:str = None
        self.mapEAssistantMessage:EvoMap = EvoMap()
        self.mapEAssistantTool:EvoMap = EvoMap()
#<
        #NOT SERIALIZED
        self.callbackParser = None
        self.callback = None
        self.arrayMessage:[] = None
        self.arrayTools:[] = None
        self.arrayToolsChoice:[] = None
#>
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteStr(self.name, stream)
        self._doWriteMap(self.mapEAssistantMessage, stream)
        self._doWriteMap(self.mapEAssistantTool, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.name = self._doReadStr(stream)
        self.mapEAssistantMessage = self._doReadMap(EAssistantMessage, stream)
        self.mapEAssistantTool = self._doReadMap(EAssistantTool, stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                f"\tsystemID:{self.systemID}",        
                f"\tname:{self.name}",
                f"\tmapEAssistantMessage:{self.mapEAssistantMessage}",
                f"\tmapEAssistantTool:{self.mapEAssistantTool}",
                            ]) 
        return strReturn

#<
     #WRAPPPER
    def addMessage(self, enumAssistantRole:EnumAssistantRole, message:str, eApiFile:EApiFile = None):
        if enumAssistantRole is None:
            raise Exception("ERROR_REQUIRED|enumAssistantRole|")
        
        if message is None:
            raise Exception("ERROR_REQUIRED|message|")
        
        eAssistantMessage = EAssistantMessage()
        eAssistantMessage.id = f"{(len(self.mapEAssistantMessage.keys()))}"
        eAssistantMessage.enumAssistantRole = enumAssistantRole
        eAssistantMessage.message = message
        self.mapEAssistantMessage.doSet(eAssistantMessage)
        
        if eAssistantMessage.enumAssistantRole == EnumAssistantRole.SYSTEM:
            self.systemID = eAssistantMessage.id
#>  