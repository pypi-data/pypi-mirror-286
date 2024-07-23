#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation    https://github.com/cyborg-ai-git # 
#========================================================================================================================================

from evo_framework import *
from evo_packages.evo_bridge_rtc_a.entity.ERtc import ERtc
from evo_packages.evo_bridge_rtc_a.entity.ERtcPeer import ERtcPeer


from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription,RTCConfiguration, RTCIceServer, RTCDataChannel, RTCCertificate
from aiortc.contrib.media import MediaBlackhole, MediaRecorder, MediaRelay, MediaPlayer
#from evo_packages.evo_package_rtc.control.MediaPlayerExt import MediaPlayerExt
class CRtcServer():  
    __instance = None

    def __init__(self):
        if CRtcServer.__instance != None:
            raise Exception("ERROR_SINGLETON")
        else:
            CRtcServer.__instance = self
            self.currentPath = os.path.dirname(os.path.abspath(__file__))
            self.maxSize:int = 160000
            self.maxConcurrentTasks:int = 8
            self.relay = MediaRelay()
            self.mapERtcPeer = EvoMap()
            self.mapFileHandler = {}
            
# ----------------------------------------------------------------------------------------------------------------------------------------  
    @staticmethod
    def getInstance():
        if CRtcServer.__instance == None:
            cObject = CRtcServer() 
        return CRtcServer.__instance
# ----------------------------------------------------------------------------------------------------------------------------------------  
    async def doInit(self):
        try:
            pass
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ----------------------------------------------------------------------------------------------------------------------------------------      
    async def getIceServer(self):
        try:
            #https://cyborgai.metered.live/api/v1/turn/credentials?apiKey=11eb58f6162f7cf291971c235fc7e4f37008
            ice_servers = [
                RTCIceServer(urls="stun:stun.relay.metered.ca:80"),
                RTCIceServer( urls =[
                                        "turn:global.relay.metered.ca:80",
                                        "turn:global.relay.metered.ca:80?transport=tcp" ,
                                        "turn:global.relay.metered.ca:443" ,
                                        "turns:global.relay.metered.ca:443?transport=tcp"
                                    ], 
                                    username = "b1f0d1fa689a93d1acd30e7c", credential = "LaSUHHu3HdZkiuAM"),
            ]
            
            IuLog.doDebug(__name__,f"ice_servers:{ ice_servers}")
        
            return ice_servers
        
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ----------------------------------------------------------------------------------------------------------------------------------------     
    async def doAction(self, eRtcPeer:ERtcPeer, channel:RTCDataChannel, data:bytes):
        try:
            idERequest, dataInput = await CApiFlow.getInstance().onRequest(data)
          
            eApiAction:EAction = IuApi.toEObject(EAction(), dataInput)
            IuLog.doVerbose(__name__,f"eRequest:{eApiAction.toString()}")
           
            eActionTask = EActionTask()
            eActionTask.id = idERequest
            eActionTask.doGenerateTime()  
            eActionTask.action = eApiAction.action
            eActionTask.eActionInput = eApiAction
            eActionTask.context = channel
            eActionTask.evoContext = eRtcPeer
            eActionTask.evoCallback = self.doneAction   
                   
            IuLog.doInfo(__name__,f"eAction:{eActionTask.toString()}")       
            await CApiFlow.getInstance().doActionCallBack(eActionTask)
                         
        except Exception as exception:
            IuLog.doException(__name__,exception)
            dataResponse = IuApi.toEResponse(idERequest, data=f"{exception}".encode())
            channel.send(dataResponse)
            channel.close()  
# ----------------------------------------------------------------------------------------------------------------------------------------      
    async def doneAction(self,eAction:EActionTask):
        try:
            channel = eAction.context
            dataOutput = eAction.eActionOutput.toBytes()
            await self.doSendResponseChunk(eAction.id, channel, dataOutput)               
        except Exception as exception:
            IuLog.doException(__name__,exception)
            dataResponse = IuApi.toEResponse(eAction.id, data=f"{exception}".encode())
            channel.send(dataResponse)
            channel.close() 
# ----------------------------------------------------------------------------------------------------------------------------------------          
    async def doTTS(self, eRtcPeer:ERtcPeer, channel:RTCDataChannel, data:bytes):
        try:          
            idERequest, dataInput = await CApiFlow.getInstance().onRequest(data)
            eApiAction:EAction = IuApi.toEObject(EAction(), dataInput)
            eApiAction.isUrlOutput = True
            
            eActionTask = EActionTask()
            eActionTask.id = idERequest
            eActionTask.doGenerateTime() 
            eActionTask.action =  eApiAction.action
            eActionTask.eActionInput = eApiAction
            eActionTask.context = channel
            eActionTask.evoContext = eRtcPeer
            eActionTask.evoCallback = self.doneTTS     
                 
            IuLog.doInfo(__name__,f"eAction:{eActionTask.toString()}")       
            await CApiFlow.getInstance().doActionCallBack(eActionTask)
            
        except Exception as exception:
            IuLog.doException(__name__,exception)
            dataResponse = IuApi.toEResponse(eRtcPeer.id, data=f"{exception}".encode())
            channel.send(dataResponse)
# ----------------------------------------------------------------------------------------------------------------------------------------      
    async def doneTTS(self, eAction:EActionTask):
        try:
            channel = eAction.context
            eRtcPeer = eAction.evoContext
            
            if isinstance(eRtcPeer,ERtcPeer): 
                eApiTypeOut =eAction.eActionOutput.mapInput.doGet("output_audio")
                if isinstance(eApiTypeOut,EApiItem):
                    IuLog.doDebug(__name__,f"eApiTypeOut: {eApiTypeOut}")
                    outputAudio= eApiTypeOut.data.decode()
                    await eRtcPeer.cAudioTrack.addAudio(outputAudio)
                else:
                    raise Exception("ERROR_NOT_VALID_output_audio")
                #dataOutput = IuApi.toBytes(eAction.eApiMediaOutput)
                #dataResponse = IuApi.toEResponse(eAction.iD,data=dataOutput, typeApi=eAction.typeApiOutput)                                 
                #channel.send(dataResponse)    
        except Exception as exception:
            IuLog.doException(__name__,exception)
            dataResponse = IuApi.toEResponse(eAction.id, data=f"{exception}".encode())
            channel.send(dataResponse)          
# ----------------------------------------------------------------------------------------------------------------------------------------         
    async def doSTT(self, eRtcPeer:ERtcPeer, channel:RTCDataChannel, data:bytes):
        try:
            eActionTask = EActionTask()
            eActionTask.doGenerateID()
            eActionTask.doGenerateTime()  
            eActionTask.context = channel
            eActionTask.evoContext = eRtcPeer
            eActionTask.evoCallback = self.doneSTT   
                     
            if eRtcPeer.cVoskKaldiTask is None:
                 eRtcPeer.cVoskKaldiTask = CVoskKaldiTask()       
                      
            await eRtcPeer.cVoskKaldiTask.setEAction(eActionTask)
            await eRtcPeer.cVoskKaldiTask.start()
        except Exception as exception:
            IuLog.doException(__name__,exception)
            dataResponse = IuApi.toEResponse(eActionTask.id, data=f"{exception}".encode())
            channel.send(dataResponse)
# ----------------------------------------------------------------------------------------------------------------------------------------         
    async def doneSTT(self, eAction:EActionTask):
        try:
            channel = eAction.context
            dataOutput = eAction.eActionOutput.toBytes()
            dataResponse = IuApi.toEResponse(eAction.id, data=dataOutput)                                 
            channel.send(dataResponse)    
        except Exception as exception:
            IuLog.doException(__name__,exception)
            dataResponse = IuApi.toEResponse(eAction.id, data=f"{exception}".encode())
            channel.send(dataResponse)
            
# ----------------------------------------------------------------------------------------------------------------------------------------          
    async def doSendResponseChunk(self,iD:str, channel, dataOutput:bytes):
        try:
            IuLog.doDebug(__name__,f"doSendResponseChunk: {iD} {channel.label} {len(dataOutput)}")
            
           # max_concurrent_tasks = self.maxConcurrentTasks
            chunk_size = self.maxSize
            
            #semaphore = asyncio.Semaphore(max_concurrent_tasks)
            file_size = len(dataOutput)
            
            count_chunk = 1
            chunk_diff = 1 if file_size % chunk_size != 0 else 0
            chunk_total = (file_size // chunk_size) + chunk_diff
            IuLog.doVerbose(__name__,f"fileSize: {file_size}")
                        
            with BytesIO(dataOutput) as fs:
                buffer = bytearray(chunk_size)
                while True:
                    try:
                        bytes_read = fs.readinto(buffer)
                        if bytes_read == 0:
                            break
                        IuLog.doVerbose(__name__,f"bytesRead: {bytes_read}")
                        data_buffer = buffer[:bytes_read] if bytes_read < chunk_size else buffer
                        data_compress =  await CApiFlow.getInstance().onResponse(iD,data_buffer,count_chunk,chunk_total)                        
                       
                        IuLog.doInfo(__name__,f"channel send: {channel.label} {channel.readyState}")
                        channel.send(data_compress)
     
                        if count_chunk == chunk_total:
                            '''
                            if not typeApi == EnumApiType.PARTIAL: #@TODO:MULTI PART
                                IuLog.doVerbose(__name__,f"doSendResponseChunk: {channel.label} CLOSE")
                                channel.close()
                            '''
                            break                            
                        
                        count_chunk += 1
                      
                                           
                    except Exception as exception:
                        IuLog.doException(__name__,exception)
                        break
                    
        except Exception as exception:
            IuLog.doException(__name__,exception)
# ----------------------------------------------------------------------------------------------------------------------------------------           
    async def doOffer(self,eRtc:ERtc) -> ERtc:
        #try:
            from evo_bridge_webrtc.control.CRtcAudioTrack import CRtcAudioTrack
            from evo_bridge_webrtc.control.CRtcVideoTrack import CRtcVideoTrack
            from evo_api_vosk.control.CVoskKaldiTask import CVoskKaldiTask
            IuLog.doDebug(__name__,f"doOffer: {eRtc.toString()}")
            eRtcPeer = ERtcPeer()
            eRtcPeer.id = eRtc.iDOffer
            eRtcPeer.doGenerateTime()
            eRtcPeer.eRtc = eRtc
           
            offer = RTCSessionDescription(sdp=eRtc.sdpOffer, type="offer")
            
            ice_servers = await self.getIceServer()
            
            eRtcPeer.peerConnection = RTCPeerConnection(RTCConfiguration(ice_servers))

           


            intro_track = "/Users/max/Documents/GIT_HUGGINGFACE/cyborgai-api-beta/assets/female.wav"
      
            eRtcPeer.cAudioTrack = CRtcAudioTrack(intro_track)
            eRtcPeer.peerConnection.addTrack(eRtcPeer.cAudioTrack)
            
            @eRtcPeer.peerConnection.on("datachannel")
            async def on_datachannel(channel:RTCDataChannel):
                IuLog.doDebug(__name__,f"on_datachannel: { eRtcPeer.id} {channel.label}")
                
               
                @channel.on("message")      
                async def on_message(message):
                    try:
                        IuLog.doInfo(__name__,f"message:{channel.label}")
                        if str(channel.label).startswith("action_"):
                                await self.doAction(eRtcPeer=eRtcPeer, channel=channel, data=message)
                       
                        elif str(channel.label).startswith("tts_"):   
                            await self.doTTS(eRtcPeer=eRtcPeer, channel=channel, data=message)
                            
                        elif str(channel.label).startswith("stt_"):
                            await self.doSTT(eRtcPeer=eRtcPeer, channel=channel, data=message)

                    except Exception as exception:
                        IuLog.doException(__name__,exception)
                
                @channel.on("statechange")     
                def on_data_channel_state_change():
                    IuLog.doDebug(__name__,f"Data channel state is now: {channel.readyState}")
                    if channel.readyState == "closed":
                        IuLog.doDebug(__name__, "Peer has disconnected or data channel is closed.")

            @eRtcPeer.peerConnection.on("iceconnectionstatechange")
            def on_ice_connection_state_change():
                IuLog.doDebug(__name__, f"ICE connection state is now: {eRtcPeer.peerConnection.iceConnectionState}")
                if eRtcPeer.peerConnection.iceConnectionState == "disconnected" or eRtcPeer.peerConnection.iceConnectionState == "failed":
                    IuLog.doDebug(__name__, "Peer may have disconnected.")
            
            @eRtcPeer.peerConnection.on("connectionstatechange")
            async def on_connectionstatechange():
                IuLog.doDebug(__name__,f"connectionstatechange: { eRtcPeer.id} {eRtcPeer.peerConnection.connectionState}")
                if eRtcPeer.peerConnection.connectionState == "failed":
                    await eRtcPeer.peerConnection.close()
                    #self.pcs.discard(pc)

            @eRtcPeer.peerConnection.on("track")
            async def on_track(track):
                IuLog.doInfo(__name__,f"Track received : { eRtcPeer.id} {track.kind}  {track}")
                
                if track.kind == "audio":
                    IuLog.doInfo(__name__,f"Track audio : { eRtcPeer.id} {track.kind}")
                    await eRtcPeer.cVoskKaldiTask.set_audio_track(track)
            
                elif track.kind == "video":
                    '''
                    eRtc.cVideoTrack = CRtcVideoTrack(
                            self.relay.subscribe(track), 
                            transform="rotate"
                        )
                    eRtc.peerConnection.addTrack(eRtc.cVideoTrack)
                    '''
                    #if args.record_to:
                    #    recorder.addTrack(relay.subscribe(track))

                @track.on("ended")
                async def on_ended():
                    try:
                        IuLog.doInfo(__name__,f"ended: {eRtcPeer.id} {track.kind}")
                        await eRtcPeer.cVoskKaldiTask.stop()
                    except Exception as exception:
                        IuLog.doException(__name__,exception)
                    
                    #await eRtc.recorder.stop()

            # handle offer
            await eRtcPeer.peerConnection.setRemoteDescription(offer)
            #await eRtcPeer.recorder.start()

            # send answer
            answer = await eRtcPeer.peerConnection.createAnswer()
            await eRtcPeer.peerConnection.setLocalDescription(answer)
            
            eRtc.sdpAnswer = eRtcPeer.peerConnection.localDescription.sdp
            self.mapERtcPeer.doSet(eRtcPeer)    
            return eRtc
        
        #except Exception as exception:
        #    IuLog.doException(__name__,exception)
        #    raise exception
# ----------------------------------------------------------------------------------------------------------------------------------------     
    async def onShutdown(self):
        try:
            IuLog.doInfo(__name__,"onShutdown")
            
            await CApiFlow.getInstance().doStop()
            
            for ePeerTmp in self.mapERtcPeer.__dictionary.values():
                try:
                    if isinstance(ePeerTmp,ERtcPeer):
                           
                        if ePeerTmp.cAudioTrack is not None:
                            ePeerTmp.cAudioTrack.doStop()
                                  
                        await ePeerTmp.cVoskKaldiTask.stop()
                        await ePeerTmp.peerConnection.close()
                except Exception as exception:
                    IuLog.doException(__name__,exception)
           
            self.mapFileHandler.clear()
            
           # coros = [pc.close() for pc in self.pcs]
           # await asyncio.gather(*coros)
           # self.pcs.clear()
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise exception