#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation    https://github.com/cyborg-ai-git # 
#========================================================================================================================================

from evo_framework import *
from evo_package_assistant.entity import *
import importlib.util
from pathlib import Path
# ---------------------------------------------------------------------------------------------------------------------------------------
# UAssistant
# ---------------------------------------------------------------------------------------------------------------------------------------
""" UAssistant
"""
class UAssistant:  
    __instance = None

    def __init__(self):
        if UAssistant.__instance != None:
            raise Exception("ERROR_SINGLETON")
        else:
            UAssistant.__instance = self  
            self.pathAssistant:str = None
            self.eAssistantMap:EAssistantMap = None
# -----------------------------------------------------------------------------
    @staticmethod
    def getInstance():
        if UAssistant.__instance == None:
            uObject = UAssistant()
            uObject.doInit()
            
        return UAssistant.__instance
# -----------------------------------------------------------------------------
    def doInit(self):
        try:   
            try:
                pathAssistantTmp = CSetting.getInstance().doGet("CYBORGAI_PATH_ASSETS_ASSISTANT")
            except Exception as exception:
                if self.pathAssistant is None:
                    IuLog.doError(__name__, f"ERROR_REQUIRED_ENV|CYBORGAI_PATH_ASSETS_ASSISTANT")
                    pathAssistantTmp=None
                    #IuLog.doWarning(__name__, f"WARNING_ENV_CYBORGAI_PATH_ASSETS_ASSISTANT_NONE_USE_{pathAssistantTmp}")
              
            self.pathAssistant = pathAssistantTmp  
            IuLog.doVerbose(__name__, f"pathAssistant:{self.pathAssistant}")
            
            self.eAssistantMap = EAssistantMap()
            self.eAssistantMap.doGenerateID()
            
            self.__doLoadDirEAssistant()
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
        
# -----------------------------------------------------------------------------   
    def doSetEAssistant(self, eAssistant:EAssistant):
        try:
           self.eAssistantMap.mapEAssistant.doSet(eAssistant)
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
        
# -----------------------------------------------------------------------------   
    async def doGetEAssistantQuery(self, eAssistantQuery:EAssistantQuery) -> EAssistant :
        try:
            if eAssistantQuery is None:
                raise Exception("ERROR_eAssistantQuery_NONE")
            
            if eAssistantQuery.query is None:
                raise Exception("ERROR_eAssistantQuery.query_NONE")
            
            arrayQuery = eAssistantQuery.query.split("=")
            
            if len(arrayQuery) != 2 and arrayQuery[0].lower() != "id":
                raise Exception("ERROR_eAssistantQuery.query_id_NONE")
                
            eAssistantID= arrayQuery[-1]
            
            return await self.doGetEAssistant(eAssistantID)
            
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# -----------------------------------------------------------------------------   
    async def doGetEAssistant(self, id) -> EAssistant:
        try:
            if id in self.eAssistantMap.mapEAssistant.keys():
                return self.eAssistantMap.mapEAssistant.doGet(id)
            else:
                pathAssistant = f"{self.pathAssistant}/assistant_{id}.py"
                self.__doLoadEAssistant(pathAssistant)
                
                if id in self.eAssistantMap.mapEAssistant.keys():
                    return self.eAssistantMap.mapEAssistant.doGet(id)
                
                IuLog.doError(__name__,f"ERROR_NOT_FOUD_ASSISTANT:{pathAssistant}")
                
                raise Exception(f"ERROR_NOT_FOUD_ASSISTANT_{id}")
            
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# -----------------------------------------------------------------------------   
    async def doQuery(self, eAssistantQuery:EAssistantQuery) -> EAssistantMap:
        try:
            #TODO:query
            self.__doLoadDirEAssistant()
            yield self.eAssistantMap
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# -----------------------------------------------------------------------------   
    async def doDelEAssistant(self, id):
        try:
            self.eAssistantMap.mapEAssistant.doDel(id)
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
#-------------------------------------------------------------------------------
    def __doLoadDirEAssistant(self):
        try:
            if self.pathAssistant is None:
                IuLog.doError(__name__, f"ERROR_REQUIRED_ENV|CYBORGAI_PATH_ASSETS_ASSISTANT")
           
            IuLog.doVerbose(__name__, f"self.pathAssistant {self.pathAssistant}")
            
            directory = Path(self.pathAssistant)
            
            arrayFileAssistant = [str(file) for file in directory.rglob('assistant_*.py')]
            
            if len(arrayFileAssistant) == 0:
                IuLog.doWarning(__name__, f"WARNING:pathAssistant empty download assistant in {self.pathAssistant}")
            
            IuLog.doVerbose(__name__,f"arrayFileAssistant:\n{arrayFileAssistant}")

            for pathAssistant in arrayFileAssistant:
                self.__doLoadEAssistant(pathAssistant)
                
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
        
#-------------------------------------------------------------------------------
    def __doLoadEAssistant(self, pathAssistant):
        try:
            IuLog.doInfo(__name__,f"pathAssistant: {pathAssistant}")
            
            # Expand the user's home directory if ~ is used
            path = os.path.expanduser(pathAssistant)

            # Create a module spec from the file location
            spec = importlib.util.spec_from_file_location("loaded_assistant", path)

            # Create a new module based on the spec
            module = importlib.util.module_from_spec(spec)

            # Execute the module in its own namespace
            spec.loader.exec_module(module)

            # Optionally, add the module to sys.modules so it can be accessed as a normal import
            #sys.modules["loaded_assistant"] = module
            module.doAddEAssistant()
                
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
         