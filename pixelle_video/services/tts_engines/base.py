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
Base TTS Engine Interface

All TTS engines must implement this interface.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List
from pathlib import Path


@dataclass
class TTSResult:
    """Result from TTS synthesis"""
    audio_path: str
    duration: float  # seconds
    sample_rate: int = 24000
    format: str = "mp3"
    metadata: Optional[dict] = None


@dataclass
class TTSVoice:
    """TTS Voice information"""
    id: str
    name: str
    language: str
    gender: str  # "male", "female", "neutral"
    preview_url: Optional[str] = None
    attributes: Optional[dict] = None


class BaseTTSEngine(ABC):
    """Base class for all TTS engines"""
    
    def __init__(self, config: dict):
        """
        Initialize TTS engine
        
        Args:
            config: Engine-specific configuration
        """
        self.config = config
    
    @abstractmethod
    async def synthesize(
        self,
        text: str,
        voice: Optional[str] = None,
        speed: float = 1.0,
        pitch: float = 1.0,
        output_path: Optional[str] = None,
        **kwargs
    ) -> TTSResult:
        """
        Synthesize text to speech
        
        Args:
            text: Text to synthesize
            voice: Voice ID (engine-specific)
            speed: Speed multiplier (1.0 = normal)
            pitch: Pitch multiplier (1.0 = normal)
            output_path: Output file path
            **kwargs: Additional engine-specific parameters
        
        Returns:
            TTSResult with audio path and metadata
        """
        pass
    
    @abstractmethod
    async def list_voices(self, language: Optional[str] = None) -> List[TTSVoice]:
        """
        List available voices
        
        Args:
            language: Filter by language code (e.g., "vi", "en", "zh")
        
        Returns:
            List of available voices
        """
        pass
    
    @abstractmethod
    def get_engine_name(self) -> str:
        """Get engine name"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if engine is available"""
        pass
    
    def _ensure_output_dir(self, output_path: str) -> Path:
        """Ensure output directory exists"""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        return path
