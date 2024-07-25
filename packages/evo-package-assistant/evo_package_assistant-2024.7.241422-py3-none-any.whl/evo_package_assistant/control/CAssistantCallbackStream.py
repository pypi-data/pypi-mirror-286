#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation	https://github.com/cyborg-ai-git | 
#========================================================================================================================================

from evo_framework import *
import re
# ---------------------------------------------------------------------------------------------------------------------------------------
# CAssistantCallbackStream
# ---------------------------------------------------------------------------------------------------------------------------------------
"""CAssistantCallbackStream
"""
class CAssistantCallbackStream:
    def __init__(self):
        self.isParseHeader:bool = True
        self.header:str = None
        self.prefixID:str = ""
        self.messageFull:str = ""
        self.count:int = 0
        self.messageHeader:str = None
        self.headerPattern = r'\[.*?\]'
        self.isRemoveHeader:bool = True
        self.chunkHeader:int = -1
        self.totenTot:int=0
# ---------------------------------------------------------------------------------------------------------------------------------------
    """onParser
    
    """
    @abstractmethod
    def onParser(self, message:str) -> EApiText: 
        eApiText= self.doParser(message)
        return eApiText
# ---------------------------------------------------------------------------------------------------------------------------------------  
    """isHeaderComplete
    
    """
    def isHeaderComplete(self, message) ->bool:
        if not self.isParseHeader:
                self.header="no"
                return True

        if self.header is None:
            self.messageFull = "".join([self.messageFull, message])
            match = re.search(self.headerPattern, self.messageFull)
            
            if match:
                self.header=match.group().replace("[","").replace("]", "")
                self.chunkHeader = self.count
                return True
            else:
                return False
        
        return True
# ---------------------------------------------------------------------------------------------------------------------------------------
    """doParser
    
    """
    def doParser(self, message:str) -> EApiText: 
        eApiText = EApiText()
        eApiText.id = f"{self.prefixID}{self.count}"  
        messageChunk=message
        self.totenTot +=1
        eApiText.tokenTot = self.totenTot

        if message is None:
            eApiText.isComplete = True      
        else:
            if self.isHeaderComplete(message):
                eApiText.header = self.header
                if self.isRemoveHeader:
                    if self.count == self.chunkHeader:
                        messageChunk = message.replace(self.header, "")
                              
        eApiText.text = messageChunk
        self.count +=1
        return eApiText
# ---------------------------------------------------------------------------------------------------------------------------------------    
    """onMessageCreated
    'thread.message.created':
    data is a message
    Occurs when a message is created.
    """
    def onMessageCreated(self):
        pass
# ---------------------------------------------------------------------------------------------------------------------------------------
    """onMessageInProgess
    'thread.message.in_progress':
    data is a message
    Occurs when a message moves to an in_progress state.
    """
    def onMessageInProgess(self):
        pass
# ---------------------------------------------------------------------------------------------------------------------------------------
    """onMessageCompleted
    'thread.message.completed':
    data is a message
    Occurs when a message is completed.
    """
    def onMessageCompleted(self):
        pass
# ---------------------------------------------------------------------------------------------------------------------------------------
    """onMessageIncomplete
    'thread.message.incomplete':
    data is a message
    Occurs when a message ends before it is completed.
    """
    def onMessageIncomplete(self):
        pass
# ---------------------------------------------------------------------------------------------------------------------------------------
    """onThreadCreated
    'thread.created':
    data is a thread
    Occurs when a new thread is created.
    """
    def onThreadCreated(self):
        pass
# ---------------------------------------------------------------------------------------------------------------------------------------
    """onRunCreated
    'thread.run.created':
    data is a run
    Occurs when a new run is created.
    """
    def onRunCreated(self):
        pass
# ---------------------------------------------------------------------------------------------------------------------------------------
    """onRunQuequed
    'thread.run.queued':
    data is a run
    Occurs when a run moves to a queued status.
    """
    def onRunQuequed(self):
        pass
# ---------------------------------------------------------------------------------------------------------------------------------------
    """onRunInProgress
    'thread.run.in_progress':
    data is a run
    Occurs when a run moves to an in_progress status.
    """
    def onRunInProgress(self):
        pass
# ---------------------------------------------------------------------------------------------------------------------------------------
    """onRequiresAction
    'thread.run.requires_action':
    data is a run
    Occurs when a run moves to a requires_action status.
    """
    def onRunRequiresAction(self):
        pass
# ---------------------------------------------------------------------------------------------------------------------------------------
    """onRunCompleted
    'thread.run.completed':
    data is a run
    Occurs when a run is completed.
    """
    def onRunCompleted(self):
        pass
# ---------------------------------------------------------------------------------------------------------------------------------------
    """onRunIncomplete
    'thread.run.incomplete':
    data is a run
    Occurs when a run ends with status incomplete.
    """
    def onRunIncomplete(self):
        pass
# ---------------------------------------------------------------------------------------------------------------------------------------
    """onRunFailed
    'thread.run.failed':
    data is a run
    Occurs when a run fails.
    """
    def onRunFailed(self):
        pass
# ---------------------------------------------------------------------------------------------------------------------------------------
    """onRunCancelling
    'thread.run.cancelling':
    data is a run
    Occurs when a run moves to a cancelling status.
    """
    def onRunCancelling(self):
        pass
# ---------------------------------------------------------------------------------------------------------------------------------------
    """onRunCancelled
    'thread.run.cancelled':
    data is a run
    Occurs when a run is cancelled.
    """
    def onRunCancelled(self):
        pass
# ---------------------------------------------------------------------------------------------------------------------------------------
    """onRunExpired
    'thread.run.expired':
    data is a run
    Occurs when a run expires.
    """
    def onRunExpired(self):
        pass
# ---------------------------------------------------------------------------------------------------------------------------------------
    """onRunStepCreated
    'thread.run.step.created':
    data is a run step
    Occurs when a run step is created.
    """
    def onRunStepCreated(self):
        pass
# ---------------------------------------------------------------------------------------------------------------------------------------
    """onRunStepInProgress
    'thread.run.step.in_progress':
    data is a run step
    Occurs when a run step moves to an in_progress state.
    """
    def onRunStepInProgress(self):
        pass
# ---------------------------------------------------------------------------------------------------------------------------------------
    """onRunStepDelta
    'thread.run.step.delta':
    data is a run step delta
    Occurs when parts of a run step are being streamed.
    """
    def onRunStepDelta(self):
        pass
# ---------------------------------------------------------------------------------------------------------------------------------------
    """onRunStepCompleted
    'thread.run.step.completed':
    data is a run step
    Occurs when a run step is completed.
    """
    def onRunStepCompleted(self):
        pass
# ---------------------------------------------------------------------------------------------------------------------------------------
    """onRunStepFailed
    'thread.run.step.failed':
    data is a run step
    Occurs when a run step fails.
    """
    def onRunStepFailed(self):
        pass
# ---------------------------------------------------------------------------------------------------------------------------------------
    """onRunStepCancelled
    'thread.run.step.cancelled':
    data is a run step
    Occurs when a run step is cancelled.
    """
    def onRunStepCancelled(self):
        pass
# ---------------------------------------------------------------------------------------------------------------------------------------
    """onRunStepExpired
    'thread.run.step.expired':
    data is a run step
    Occurs when a run step expires.
    """
    def onRunStepExpired(self):
        pass
# ---------------------------------------------------------------------------------------------------------------------------------------
    """onError
    'error':
    data is an error
    Occurs when an error occurs. This can happen due to an internal server error or a timeout.
    """
    def onError(self):
        pass
# ---------------------------------------------------------------------------------------------------------------------------------------
    """onDone
    'done':
    data is [DONE]
    Occurs when a stream ends.
    """
    def onDone(self):
        pass  
# ---------------------------------------------------------------------------------------------------------------------------------------