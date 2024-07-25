#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation	https://github.com/cyborg-ai-git | 
#========================================================================================================================================

from evo_framework import *
from evo_package_assistant.entity import *
from evo_package_assistant.utility import *
# ---------------------------------------------------------------------------------------------------------------------------------------
# CAssistantApi
# ---------------------------------------------------------------------------------------------------------------------------------------
"""CAssistantApi
"""
class CAssistantApi(CApi):
	__instance = None
# ---------------------------------------------------------------------------------------------------------------------------------------
	def __init__(self):   
		if CAssistantApi.__instance != None:
			raise Exception("ERROR:SINGLETON")
		else:
			super().__init__()
			CAssistantApi.__instance = self
			self.current_path = os.path.dirname(os.path.abspath(__file__))
			self.path_assets:str = f"{self.current_path}/../../../../assets"
			
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""getInstance Singleton

	Raises:
		Exception:  api exception

	Returns:
		_type_: CAssistantApi instance
	"""
	@staticmethod
	def getInstance():
		if CAssistantApi.__instance is None:
			cObject = CAssistantApi()  
			cObject.doInit()  
		return CAssistantApi.__instance
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""doInit

	Raises:
		Exception: api exception

	Returns:

	"""   
	def doInit(self):   
		UAssistant.getInstance()	  
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""doAddApi

	Raises:
		Exception: api exception

	Returns:

	"""
	@override   
	def doAddApi(self):
		try:			
			
			api0 = self.newApi("assistant-set", callback=self.onSet, input=EAssistantAdmin, output=EAssistant, isEnabled=True )
			api0.description="assistant-set description"

			api1 = self.newApi("assistant-get", callback=self.onGet, input=EAssistantQuery, output=EAssistant, isEnabled=True )
			api1.description="assistant-get description"

			api2 = self.newApi("assistant-del", callback=self.onDel, input=EAssistantAdmin, output=EAssistant, isEnabled=True )
			api2.description="assistant-del description"

			api3 = self.newApi("assistant-query", callback=self.onQuery, input=EAssistantQuery, output=EAssistantMap, isEnabled=True )
			api3.description="assistant-query description"
  
		except Exception as exception:
			IuLog.doException(__name__, exception)
			raise
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""onSet api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onSet(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onSet: {eAction} ")
				
			eAssistantAdmin:EAssistantAdmin = eAction.doGetInput(EAssistantAdmin)
			
			#Remove eAction input for free memory
			eAction.input = None
#<
			#++++++++++++++++++++++++++++++++++++++++++++++++++++++++
			#@TODO: INSERT YOUR CODE 

			eAssistant = EAssistant()
			eAssistant.doGenerateID()

			eAction.doSetOutput(eAssistant)
			
		  

			return eAction
			#++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#>

		except Exception as exception:
			IuLog.doException(__name__, exception)
			raise
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""onGet api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onGet(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onGet: {eAction} ")
				
			eAssistantQuery:EAssistantQuery = eAction.doGetInput(EAssistantQuery)
			
			#Remove eAction input for free memory
			eAction.input = None
#<
			eAssistant = await UAssistant.getInstance().doGetEAssistantQuery(eAssistantQuery)
			eAction.doSetOutput(eAssistant)
			yield eAction
			'''
			async for eAssistant in UAssistant.getInstance().doGetEAssistantQuery(eAssistantQuery):
				eAction.doSetOutput(eAssistant)
				yield eAction
    
			'''
#>
		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction


# ---------------------------------------------------------------------------------------------------------------------------------------
	"""onDel api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onDel(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onDel: {eAction} ")
				
			eAssistantAdmin:EAssistantAdmin = eAction.doGetInput(EAssistantAdmin)
			
			#Remove eAction input for free memory
			eAction.input = None
#<
			#++++++++++++++++++++++++++++++++++++++++++++++++++++++++
			#@TODO: INSERT YOUR CODE 

			eAssistant = EAssistant()
			eAssistant.doGenerateID()

			eAction.doSetOutput(eAssistant)
			
		  

			return eAction
			#++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#>

		except Exception as exception:
			IuLog.doException(__name__, exception)
			raise
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""onQuery api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onQuery(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onQuery: {eAction} ")
				
			eAssistantQuery:EAssistantQuery = eAction.doGetInput(EAssistantQuery)
			
			#Remove eAction input for free memory
			eAction.input = None
   
#<			

			async for eAssistantMap in UAssistant.getInstance().doQuery(eAssistantQuery):
				eAction.doSetOutput(eAssistantMap)
				yield eAction		
#>
		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------