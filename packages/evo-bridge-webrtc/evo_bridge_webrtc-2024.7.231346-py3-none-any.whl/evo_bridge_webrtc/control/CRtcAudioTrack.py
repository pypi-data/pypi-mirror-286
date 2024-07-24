#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation    https://github.com/cyborg-ai-git # 
#========================================================================================================================================

from aiortc import MediaStreamTrack
import asyncio
from aiortc.contrib.media import MediaPlayer
from aiortc.mediastreams import AudioStreamTrack
from evo_framework.core.evo_core_log.utility.IuLog import IuLog
from aiortc.mediastreams import MediaStreamError
import av

class CRtcAudioTrack(MediaStreamTrack):
    kind = "audio"

    def __init__(self, audioFile: str):
        super().__init__()
        self.currentMediaPlayer = MediaPlayer(audioFile)
        self.arrayAudioFile = []
        self.isRunning = True
        self.last_pts = 0 

    async def addAudio(self, audioFile: str):
        IuLog.doVerbose(__name__, f"addAudio: {audioFile}") 
        self.arrayAudioFile.append(audioFile)

    async def doStop(self):
        self.isRunning = False

    async def recv(self):
        while self.isRunning:         
            if not self.currentMediaPlayer and len(self.arrayAudioFile) > 0:
                audioFile = self.arrayAudioFile.pop(0)
                self.currentMediaPlayer = MediaPlayer(audioFile)
                IuLog.doVerbose(__name__, f"Playing: {audioFile}") 
                    
            elif self.currentMediaPlayer:  
                try:
                    frame = await self.currentMediaPlayer.audio.recv()
                    # Adjust the frame's PTS based on the last known PTS
                    if frame is not None:
                        frame.pts = self.last_pts + frame.samples
                        self.last_pts = frame.pts
                        return frame      
                except MediaStreamError as exception:
                    IuLog.doVerbose(__name__, f"end MediaStreamError: {exception}")  
                    self.currentMediaPlayer = None
            else:  
                await asyncio.sleep(0.01)