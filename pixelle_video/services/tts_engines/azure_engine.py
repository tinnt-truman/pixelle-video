# Copyright (C) 2025 AIDC-AI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Azure Cognitive Services TTS Engine

Microsoft Azure Speech Services - High quality, enterprise-grade TTS.
Requires Azure subscription.
"""

import uuid
from pathlib import Path
from typing import Optional, List

from loguru import logger

from .base import BaseTTSEngine, TTSResult, TTSVoice


class AzureTTSEngine(BaseTTSEngine):
    """Azure Cognitive Services TTS engine"""
    
    # Vietnamese voices
    VOICES = [
        {"id": "vi-VN-HoaiMyNeural", "name": "HoaiMy (Female)", "language": "vi", "gender": "female"},
        {"id": "vi-VN-NamMinhNeural", "name": "NamMinh (Male)", "language": "vi", "gender": "male"},
        {"id": "en-US-JennyNeural", "name": "Jenny (Female)", "language": "en", "gender": "female"},
        {"id": "en-US-GuyNeural", "name": "Guy (Male)", "language": "en", "gender": "male"},
        {"id": "zh-CN-XiaoxiaoNeural", "name": "Xiaoxiao (Female)", "language": "zh", "gender": "female"},
        {"id": "zh-CN-YunxiNeural", "name": "Yunxi (Male)", "language": "zh", "gender": "male"},
    ]
    
    def __init__(self, config: dict = None):
        super().__init__(config or {})
        self.subscription_key = self.config.get("subscription_key", "")
        self.region = self.config.get("region", "eastasia")
        self.endpoint = self.config.get("endpoint", "")
    
    async def synthesize(
        self,
        text: str,
        voice: Optional[str] = None,
        speed: float = 1.0,
        pitch: float = 1.0,
        output_path: Optional[str] = None,
        **kwargs
    ) -> TTSResult:
        """Synthesize text using Azure TTS"""
        if not self.is_available():
            raise ValueError("Azure TTS not configured. Set subscription_key and region.")
        
        # Determine voice
        if not voice:
            voice = self.config.get("voice", "vi-VN-HoaiMyNeural")
        
        # Generate output path
        if not output_path:
            output_path = f"output/tts/{uuid.uuid4().hex}.mp3"
        
        self._ensure_output_dir(output_path)
        
        logger.info(f"Azure TTS: voice={voice}, speed={speed}")
        
        try:
            # Try to use Azure Speech SDK if available
            try:
                import azure.cognitiveservices.speech as speechsdk
                
                return await self._synthesize_with_sdk(
                    text=text,
                    voice=voice,
                    speed=speed,
                    pitch=pitch,
                    output_path=output_path
                )
            except ImportError:
                logger.warning("Azure Speech SDK not installed, using REST API")
                return await self._synthesize_with_rest(
                    text=text,
                    voice=voice,
                    speed=speed,
                    pitch=pitch,
                    output_path=output_path
                )
            
        except Exception as e:
            logger.error(f"Azure TTS error: {e}")
            raise
    
    async def _synthesize_with_sdk(
        self,
        text: str,
        voice: str,
        speed: float,
        pitch: float,
        output_path: str
    ) -> TTSResult:
        """Synthesize using Azure Speech SDK"""
        import azure.cognitiveservices.speech as speechsdk
        
        # Configure speech synthesis
        speech_config = speechsdk.SpeechConfig(
            subscription=self.subscription_key,
            region=self.region
        )
        
        # Set voice
        speech_config.speech_synthesis_voice_name = voice
        
        # Set speed (SSML)
        rate_percentage = int((speed - 1.0) * 100)
        rate_str = f"+{rate_percentage}%" if rate_percentage >= 0 else f"{rate_percentage}%"
        
        # Create audio config
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)
        
        # Create synthesizer
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=audio_config
        )
        
        # Synthesize
        result = synthesizer.speak_text_async(text).get()
        
        if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            raise Exception(f"Azure TTS failed: {result.reason}")
        
        # Get duration
        duration = self._estimate_duration(text, speed)
        
        return TTSResult(
            audio_path=output_path,
            duration=duration,
            sample_rate=24000,
            format="mp3",
            metadata={"voice": voice, "speed": speed}
        )
    
    async def _synthesize_with_rest(
        self,
        text: str,
        voice: str,
        speed: float,
        pitch: float,
        output_path: str
    ) -> TTSResult:
        """Synthesize using Azure REST API"""
        import httpx
        
        # Build SSML
        rate_percentage = int((speed - 1.0) * 100)
        rate_str = f"+{rate_percentage}%" if rate_percentage >= 0 else f"{rate_percentage}%"
        
        ssml = f"""
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='vi-VN'>
            <voice name='{voice}'>
                <prosody rate='{rate_str}'>
                    {text}
                </prosody>
            </voice>
        </speak>
        """
        
        # Make request
        url = f"https://{self.region}.tts.speech.microsoft.com/cognitiveservices/v1"
        headers = {
            "Ocp-Apim-Subscription-Key": self.subscription_key,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-24khz-48kbitrate-mono-mp3"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                content=ssml,
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            
            # Save audio
            with open(output_path, "wb") as f:
                f.write(response.content)
        
        # Get duration
        duration = self._estimate_duration(text, speed)
        
        return TTSResult(
            audio_path=output_path,
            duration=duration,
            sample_rate=24000,
            format="mp3",
            metadata={"voice": voice, "speed": speed}
        )
    
    async def list_voices(self, language: Optional[str] = None) -> List[TTSVoice]:
        """List available Azure voices"""
        voices = []
        
        for v in self.VOICES:
            if language and not v["language"].startswith(language):
                continue
            
            voices.append(TTSVoice(
                id=v["id"],
                name=v["name"],
                language=v["language"],
                gender=v["gender"]
            ))
        
        return voices
    
    def get_engine_name(self) -> str:
        return "azure_tts"
    
    def is_available(self) -> bool:
        return bool(self.subscription_key and self.region)
    
    def _estimate_duration(self, text: str, speed: float) -> float:
        """Estimate audio duration from text"""
        words = len(text.split())
        minutes = words / 150
        seconds = minutes * 60 / speed
        return max(1.0, seconds)
