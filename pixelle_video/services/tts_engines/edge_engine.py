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
Edge TTS Engine

Microsoft Edge TTS - Free, fast, good quality.
Supports many languages including Vietnamese.
"""

import uuid
from pathlib import Path
from typing import Optional, List

import edge_tts
from loguru import logger

from .base import BaseTTSEngine, TTSResult, TTSVoice


class EdgeTTSEngine(BaseTTSEngine):
    """Microsoft Edge TTS engine"""
    
    # Default Vietnamese voices
    DEFAULT_VOICES = {
        "vi": "vi-VN-HoaiMyNeural",
        "en": "en-US-JennyNeural",
        "zh": "zh-CN-XiaoxiaoNeural",
    }
    
    def __init__(self, config: dict = None):
        super().__init__(config or {})
        self.proxy = self.config.get("proxy")
    
    async def synthesize(
        self,
        text: str,
        voice: Optional[str] = None,
        speed: float = 1.0,
        pitch: float = 1.0,
        output_path: Optional[str] = None,
        **kwargs
    ) -> TTSResult:
        """Synthesize text using Edge TTS"""
        # Determine voice
        if not voice:
            voice = self.config.get("voice", "vi-VN-HoaiMyNeural")
        
        # Convert speed to rate string
        rate = self._speed_to_rate(speed)
        pitch_str = self._pitch_to_string(pitch)
        
        # Generate output path
        if not output_path:
            output_path = f"output/tts/{uuid.uuid4().hex}.mp3"
        
        self._ensure_output_dir(output_path)
        
        logger.info(f"Edge TTS: voice={voice}, rate={rate}")
        
        try:
            communicate = edge_tts.Communicate(
                text=text,
                voice=voice,
                rate=rate,
                pitch=pitch_str,
                proxy=self.proxy
            )
            
            await communicate.save(output_path)
            
            # Get duration (approximate)
            duration = self._estimate_duration(text, speed)
            
            return TTSResult(
                audio_path=output_path,
                duration=duration,
                sample_rate=24000,
                format="mp3",
                metadata={"voice": voice, "rate": rate}
            )
            
        except Exception as e:
            logger.error(f"Edge TTS error: {e}")
            raise
    
    async def list_voices(self, language: Optional[str] = None) -> List[TTSVoice]:
        """List available Edge TTS voices"""
        voices = []
        
        try:
            voice_list = await edge_tts.list_voices(proxy=self.proxy)
            
            for v in voice_list:
                if language and not v["Locale"].startswith(language):
                    continue
                
                voices.append(TTSVoice(
                    id=v["ShortName"],
                    name=v["FriendlyName"],
                    language=v["Locale"],
                    gender=v["Gender"],
                    attributes={
                        "voice_type": v.get("VoiceType"),
                        "status": v.get("Status"),
                    }
                ))
                
        except Exception as e:
            logger.error(f"Failed to list Edge TTS voices: {e}")
        
        return voices
    
    def get_engine_name(self) -> str:
        return "edge_tts"
    
    def is_available(self) -> bool:
        return True
    
    def _speed_to_rate(self, speed: float) -> str:
        """Convert speed multiplier to rate string"""
        # speed: 1.0 = normal, 1.2 = 20% faster
        # rate: "+0%" = normal, "+20%" = faster
        percentage = int((speed - 1.0) * 100)
        if percentage >= 0:
            return f"+{percentage}%"
        return f"{percentage}%"
    
    def _pitch_to_string(self, pitch: float) -> str:
        """Convert pitch multiplier to string"""
        # pitch: 1.0 = normal
        # Hz: "+0Hz" = normal
        hz = int((pitch - 1.0) * 50)  # rough conversion
        if hz >= 0:
            return f"+{hz}Hz"
        return f"{hz}Hz"
    
    def _estimate_duration(self, text: str, speed: float) -> float:
        """Estimate audio duration from text"""
        # Rough estimate: ~150 words per minute at normal speed
        words = len(text.split())
        minutes = words / 150
        seconds = minutes * 60 / speed
        return max(1.0, seconds)
