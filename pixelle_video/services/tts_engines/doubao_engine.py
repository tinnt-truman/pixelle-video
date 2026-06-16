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
Doubao TTS Engine

ByteDance Doubao TTS - High quality Chinese TTS.
Requires API credentials from Volcengine.
"""

import uuid
import hmac
import hashlib
import json
import time
from pathlib import Path
from typing import Optional, List
from datetime import datetime

import httpx
from loguru import logger

from .base import BaseTTSEngine, TTSResult, TTSVoice


class DoubaoTTSEngine(BaseTTSEngine):
    """ByteDance Doubao TTS engine"""
    
    # Volcengine TTS API endpoints
    API_ENDPOINT = "https://openspeech.bytedance.com/api/v1/tts"
    
    # Available voices
    VOICES = [
        {"id": "zh_female_shuangkuaisisi_moon_bigtts", "name": "女-爽快思思", "language": "zh", "gender": "female"},
        {"id": "zh_male_chunhou_moon_bigtts", "name": "男-醇厚", "language": "zh", "gender": "male"},
        {"id": "zh_female_tianmei_moon_bigtts", "name": "女-甜美", "language": "zh", "gender": "female"},
        {"id": "zh_male_jingying_moon_bigtts", "name": "男-精英", "language": "zh", "gender": "male"},
        {"id": "zh_female_wennuan_moon_bigtts", "name": "女-温暖", "language": "zh", "gender": "female"},
        {"id": "zh_male_yangguang_moon_bigtts", "name": "男-阳光", "language": "zh", "gender": "male"},
    ]
    
    def __init__(self, config: dict = None):
        super().__init__(config or {})
        self.appid = self.config.get("appid", "")
        self.token = self.config.get("token", "")
        self.access_token = self.config.get("access_token", "")
        self.cluster = self.config.get("cluster", "volcano_tts")
        self.api_url = self.config.get("api_url", self.API_ENDPOINT)
    
    async def synthesize(
        self,
        text: str,
        voice: Optional[str] = None,
        speed: float = 1.0,
        pitch: float = 1.0,
        output_path: Optional[str] = None,
        **kwargs
    ) -> TTSResult:
        """Synthesize text using Doubao TTS"""
        if not self.is_available():
            raise ValueError("Doubao TTS not configured. Set appid and access_token.")
        
        # Determine voice
        if not voice:
            voice = self.config.get("voice", "zh_female_shuangkuaisisi_moon_bigtts")
        
        # Generate output path
        if not output_path:
            output_path = f"output/tts/{uuid.uuid4().hex}.mp3"
        
        self._ensure_output_dir(output_path)
        
        logger.info(f"Doubao TTS: voice={voice}, speed={speed}")
        
        try:
            # Prepare request
            payload = {
                "app": {
                    "appid": self.appid,
                    "token": "access_token",
                    "cluster": self.cluster
                },
                "user": {
                    "uid": str(uuid.uuid4().hex)
                },
                "audio": {
                    "voice_type": voice,
                    "encoding": "mp3",
                    "speed_ratio": speed,
                    "volume_ratio": 1.0,
                    "pitch_ratio": pitch,
                },
                "request": {
                    "reqid": str(uuid.uuid4().hex),
                    "text": text,
                    "text_type": "plain",
                    "operation": "query",
                    "with_frontend": 1,
                    "frontend_type": "unitTson"
                }
            }
            
            # Make request
            headers = {
                "Authorization": f"Bearer;{self.access_token}",
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    json=payload,
                    headers=headers,
                    timeout=30.0
                )
                response.raise_for_status()
                
                result = response.json()
                
                if result.get("code") != 3000:
                    raise Exception(f"Doubao TTS error: {result.get('message', 'Unknown error')}")
                
                # Decode audio data
                import base64
                audio_data = base64.b64decode(result["data"])
                
                # Save to file
                with open(output_path, "wb") as f:
                    f.write(audio_data)
            
            # Get duration
            duration = self._estimate_duration(text, speed)
            
            return TTSResult(
                audio_path=output_path,
                duration=duration,
                sample_rate=24000,
                format="mp3",
                metadata={"voice": voice, "speed": speed}
            )
            
        except Exception as e:
            logger.error(f"Doubao TTS error: {e}")
            raise
    
    async def list_voices(self, language: Optional[str] = None) -> List[TTSVoice]:
        """List available Doubao voices"""
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
        return "doubao_tts"
    
    def is_available(self) -> bool:
        return bool(self.appid and self.access_token)
    
    def _estimate_duration(self, text: str, speed: float) -> float:
        """Estimate audio duration from text"""
        # Chinese: ~4 characters per second at normal speed
        chars = len(text)
        seconds = chars / 4 / speed
        return max(1.0, seconds)
