#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation	https://github.com/cyborg-ai-git | 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_framework.core.evo_core_api.entity.EApiAdmin import EApiAdmin
from evo_package_assistant.entity.EAssistantMessage import EAssistantMessage
#========================================================================================================================================
"""EAssistantAdmin

	EAssistantAdmin DESCRIPTION
	
"""
class EAssistantAdmin(EObject):

	VERSION:str="683cafa6f5264a05f1b74a80cd882f81fe8d5e594509e256b31057e94095e115"

	def __init__(self):
		super().__init__()
		
		self.eApiAdmin:EApiAdmin = None
		self.eAssistantMessage:EAssistantMessage = None
  
	def toStream(self, stream):
		super().toStream(stream)
		
		self._doWriteEObject(self.eApiAdmin, stream)
		self._doWriteEObject(self.eAssistantMessage, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		
		self.eApiAdmin = self._doReadEObject(EApiAdmin, stream)
		self.eAssistantMessage = self._doReadEObject(EAssistantMessage, stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),
							
				f"\teApiAdmin:{self.eApiAdmin}",
				f"\teAssistantMessage:{self.eAssistantMessage}",
							]) 
		return strReturn
	