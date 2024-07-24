#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation	https://github.com/cyborg-ai-git | 
#========================================================================================================================================

from evo_framework import *
from evo_bridge_webrtc.entity import *
from evo_bridge_webrtc.utility import *

# ---------------------------------------------------------------------------------------------------------------------------------------
# CWebrtcApi
# ---------------------------------------------------------------------------------------------------------------------------------------
"""CWebrtcApi
"""
class CWebrtcApi(CApi):
	__instance = None
# ---------------------------------------------------------------------------------------------------------------------------------------
	def __init__(self):   
		if CWebrtcApi.__instance != None:
			raise Exception("ERROR:SINGLETON")
		else:
			super().__init__()
			CWebrtcApi.__instance = self
			self.currentPath = os.path.dirname(os.path.abspath(__file__))
			
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""getInstance Singleton

	Raises:
		Exception:  api exception

	Returns:
		_type_: CWebrtcApi instance
	"""
	@staticmethod
	def getInstance():
		if CWebrtcApi.__instance is None:
			cObject = CWebrtcApi()  
			cObject.doInit()  
		return CWebrtcApi.__instance
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""doInit

	Raises:
		Exception: api exception

	Returns:

	"""   
	def doInit(self):   
		try:			
			UWebrtcApi.getInstance()
		except Exception as exception:
			IuLog.doException(__name__, exception)
			raise	  
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""doAddApi

	Raises:
		Exception: api exception

	Returns:

	"""
	@override   
	def doAddApi(self):
		try:			
			
			api0 = self.newApi("webrtc-get_sdp_answer", callback=self.onGetSdpAnswer, input=ERtc, output=ERtc )
			api0.description="webrtc-get_sdp_answer _DESCRIPTION_"
			api0.required="*"
  
		except Exception as exception:
			IuLog.doException(__name__, exception)
			raise
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""onGetSdpAnswer api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onGetSdpAnswer(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onGetSdpAnswer: {eAction} ")
				
			eRtcInput:ERtc = eAction.doGetInput(ERtc)
			
			#Remove eAction input for free memory
			eAction.input = None
					
			async for eRtcOutput in UWebrtcApi.getInstance().doOnGetSdpAnswer(eRtcInput):
				eAction.doSetOutput(eRtcOutput)
				yield eAction	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------
