#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation    https://github.com/cyborg-ai-git | 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_bridge_webrtc.entity.ERtc import ERtc
#<
from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription,RTCConfiguration, RTCIceServer
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder, MediaRelay
#>
#========================================================================================================================================
"""ERtcPeer

    EWebrtcOutput _DOC_
    
"""
class ERtcPeer(EObject):

    VERSION:str="b8bfd7b507f3b296d2d8bf275eb5c04a1f2a8b0849e5dfa07d8d5c4ed5d3e9d5"

    def __init__(self):
        super().__init__()
        
        self.eRtc:ERtc = None
        
#<
        self.peerConnection:RTCPeerConnection = None
        self.mediaPlayerAudio:MediaPlayer = None
        self.recorder = MediaBlackhole()
        self.cAudioTrack = None
        self.cVideoTrack = None
        self.cVoskKaldiTask = None
        self.isWaitAnswer:bool = False
#>
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteEObject(self.eRtc, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.eRtc = self._doReadEObject(ERtc, stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\teRtc:{self.eRtc}",
                            ]) 
        return strReturn

#<
    async def setup_audio_track(self, audio_file_path):
        print(f"setup_audio_track : {audio_file_path}")
        self.mediaPlayerAudio = MediaPlayer(audio_file_path)
        await self.cAudioTrack.setTrack(self.mediaPlayerAudio.audio)
       # print(f"setup_audio_track : {audio_file_path} play")
        #self.peerConnection.addTrack(self.cAudioTrack)
        #self.mediaPlayerAudio.audio.play()
        
        #self.peerConnection.addTrack(self.mediaPlayerAudio.audio)
       
        #self.cAudioTrack = CAudioTrack(self.mediaPlayerAudio.audio)
        #self.peerConnection.addTrack(self.cAudioTrack)
        
        print(f"setup_audio_track : {audio_file_path} play")
        '''
        if original_audio_track:
            print(f"\n\nsetup_audio_track : {original_audio_track}")
            self.cAudioTrack = CAudioTrack(original_audio_track)
            self.peerConnection.addTrack(self.cAudioTrack)
        '''
    async def stop_current_audio_track(self):
        if self.cAudioTrack:
            print("stop_current_audio_track")
            self.mediaPlayerAudio.audio.stop()
            #self.cAudioTrack.stop()  # Assuming your CAudioTrack class has a stop method to handle any cleanup
            #self.cAudioTrack = None

    async def send_new_audio(self, audio_file_path):
        print(f"\n\nsend_new_audio : {audio_file_path}")
        await self.stop_current_audio_track()
        await self.setup_audio_track(audio_file_path)    
        
#>