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
IndexTTS Engine

Voice cloning TTS - Clone any voice from reference audio.
Requires IndexTTS server running locally or remotely.
"""

import uuid
from pathlib import Path
from typing import Optional, List

import httpx
from loguru import logger

from .base import BaseTTSEngine, TTSResult, TTSVoice


class IndexTTSEngine(BaseTTSEngine):
    """IndexTTS voice cloning engine"""
    
    def __init__(self, config: dict = None):
        super().__init__(config or {})
        self.server_url = self.config.get("server_url", "http://127.0.0.1:5000")
        self.timeout = self.config.get("timeout", 120)
    
    async def synthesize(
        self,
        text: str,
        voice: Optional[str] = None,
        speed: float = 1.0,
        pitch: float = 1.0,
        output_path: Optional[str] = None,
        ref_audio: Optional[str] = None,
        **kwargs
    ) -> TTSResult:
        """
        Synthesize text using IndexTTS with voice cloning
        
        Args:
            text: Text to synthesize
            voice: Voice ID (not used, use ref_audio instead)
            speed: Speed multiplier
            pitch: Pitch multiplier
            output_path: Output file path
            ref_audio: Path to reference audio for voice cloning
        """
        if not self.is_available():
            raise ValueError(f"IndexTTS server not available at {self.server_url}")
        
        if not ref_audio:
            raise ValueError("IndexTTS requires ref_audio for voice cloning")
        
        # Generate output path
        if not output_path:
            output_path = f"output/tts/{uuid.uuid4().hex}.wav"
        
        self._ensure_output_dir(output_path)
        
        logger.info(f"IndexTTS: cloning voice from {ref_audio}")
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Upload reference audio
                with open(ref_audio, "rb") as f:
                    files = {"audio": (ref_audio, f, "audio/wav")}
                    data = {"text": text}
                    
                    response = await client.post(
                        f"{self.server_url}/clone",
                        files=files,
                        data=data
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
                sample_rate=22050,
                format="wav",
                metadata={"ref_audio": ref_audio, "voice_cloned": True}
            )
            
        except Exception as e:
            logger.error(f"IndexTTS error: {e}")
            raise
    
    async def list_voices(self, language: Optional[str] = None) -> List[TTSVoice]:
        """List available voices (IndexTTS uses voice cloning)"""
        # IndexTTS doesn't have predefined voices
        # Return empty list or custom voices from config
        return []
    
    def get_engine_name(self) -> str:
        return "index_tts"
    
    def is_available(self) -> bool:
        """Check if IndexTTS server is running"""
        try:
            import httpx
            response = httpx.get(f"{self.server_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _estimate_duration(self, text: str, speed: float) -> float:
        """Estimate audio duration from text"""
        words = len(text.split())
        minutes = words / 150
        seconds = minutes * 60 / speed
        return max(1.0, seconds)
