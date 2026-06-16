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
Subtitle Service

Generate subtitles from audio/video files using Whisper.
Supports multiple languages including Vietnamese.
"""

import os
import uuid
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass

from loguru import logger


@dataclass
class SubtitleSegment:
    """A single subtitle segment"""
    index: int
    start_time: float
    end_time: float
    text: str


@dataclass
class SubtitleResult:
    """Result from subtitle generation"""
    srt_path: str
    segments: List[SubtitleSegment]
    language: str
    duration: float


class SubtitleService:
    """Subtitle generation service using Whisper"""
    
    def __init__(self, config: dict = None):
        """
        Initialize subtitle service
        
        Args:
            config: Configuration dict with:
                - model_size: Whisper model size (default: "base")
                - device: "cpu" or "cuda" (default: "cpu")
                - language: Default language code (default: "vi")
        """
        self.config = config or {}
        self.model_size = self.config.get("model_size", "base")
        self.device = self.config.get("device", "cpu")
        self.language = self.config.get("language", "vi")
        self._model = None
    
    def _load_model(self):
        """Lazy load Whisper model"""
        if self._model is not None:
            return
        
        try:
            import whisper
            logger.info(f"Loading Whisper model: {self.model_size}")
            self._model = whisper.load_model(self.model_size, device=self.device)
            logger.info("Whisper model loaded successfully")
        except ImportError:
            raise ImportError(
                "Whisper not installed. Run: pip install openai-whisper"
            )
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            raise
    
    async def generate(
        self,
        audio_path: str,
        output_path: Optional[str] = None,
        language: Optional[str] = None,
        **kwargs
    ) -> SubtitleResult:
        """
        Generate subtitles from audio file
        
        Args:
            audio_path: Path to audio/video file
            output_path: Output SRT file path
            language: Language code (e.g., "vi", "en", "zh")
        
        Returns:
            SubtitleResult with SRT file and segments
        """
        self._load_model()
        
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Generate output path
        if not output_path:
            output_path = f"output/subtitles/{uuid.uuid4().hex}.srt"
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        lang = language or self.language
        
        logger.info(f"Generating subtitles: {audio_path} -> {output_path}")
        
        try:
            # Transcribe
            result = self._model.transcribe(
                audio_path,
                language=lang,
                word_timestamps=True,
                verbose=False
            )
            
            # Convert to SRT format
            segments = []
            srt_lines = []
            
            for i, segment in enumerate(result["segments"], 1):
                start = segment["start"]
                end = segment["end"]
                text = segment["text"].strip()
                
                if not text:
                    continue
                
                # Create segment
                seg = SubtitleSegment(
                    index=i,
                    start_time=start,
                    end_time=end,
                    text=text
                )
                segments.append(seg)
                
                # Add to SRT
                srt_lines.append(f"{i}")
                srt_lines.append(f"{self._format_time(start)} --> {self._format_time(end)}")
                srt_lines.append(text)
                srt_lines.append("")
            
            # Write SRT file
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("\n".join(srt_lines))
            
            # Get duration
            duration = segments[-1].end_time if segments else 0
            
            logger.info(f"✅ Generated {len(segments)} subtitle segments")
            
            return SubtitleResult(
                srt_path=output_path,
                segments=segments,
                language=lang,
                duration=duration
            )
            
        except Exception as e:
            logger.error(f"Subtitle generation error: {e}")
            raise
    
    def _format_time(self, seconds: float) -> str:
        """Format seconds to SRT timestamp (HH:MM:SS,mmm)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        millis = int((secs % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{int(secs):02d},{millis:03d}"
    
    async def translate(
        self,
        srt_path: str,
        target_language: str,
        output_path: Optional[str] = None
    ) -> str:
        """
        Translate SRT file to another language
        
        Args:
            srt_path: Input SRT file path
            target_language: Target language code
            output_path: Output SRT file path
        
        Returns:
            Path to translated SRT file
        """
        # TODO: Implement translation using LLM
        # For now, just copy the file
        if not output_path:
            output_path = srt_path.replace(".srt", f".{target_language}.srt")
        
        import shutil
        shutil.copy2(srt_path, output_path)
        
        return output_path
    
    async def merge(
        self,
        srt_paths: List[str],
        output_path: str
    ) -> str:
        """
        Merge multiple SRT files into one
        
        Args:
            srt_paths: List of SRT file paths
            output_path: Output merged SRT file path
        
        Returns:
            Path to merged SRT file
        """
        all_segments = []
        
        for path in srt_paths:
            segments = self._parse_srt(path)
            all_segments.extend(segments)
        
        # Sort by start time
        all_segments.sort(key=lambda x: x.start_time)
        
        # Re-index
        for i, seg in enumerate(all_segments, 1):
            seg.index = i
        
        # Write merged SRT
        srt_lines = []
        for seg in all_segments:
            srt_lines.append(f"{seg.index}")
            srt_lines.append(f"{self._format_time(seg.start_time)} --> {self._format_time(seg.end_time)}")
            srt_lines.append(seg.text)
            srt_lines.append("")
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(srt_lines))
        
        return output_path
    
    def _parse_srt(self, srt_path: str) -> List[SubtitleSegment]:
        """Parse SRT file into segments"""
        segments = []
        
        with open(srt_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Split by double newline
        blocks = content.strip().split("\n\n")
        
        for block in blocks:
            lines = block.strip().split("\n")
            if len(lines) < 3:
                continue
            
            try:
                index = int(lines[0])
                time_parts = lines[1].split(" --> ")
                start = self._parse_time(time_parts[0])
                end = self._parse_time(time_parts[1])
                text = "\n".join(lines[2:])
                
                segments.append(SubtitleSegment(
                    index=index,
                    start_time=start,
                    end_time=end,
                    text=text
                ))
            except Exception as e:
                logger.warning(f"Failed to parse SRT block: {e}")
                continue
        
        return segments
    
    def _parse_time(self, time_str: str) -> float:
        """Parse SRT timestamp to seconds"""
        # Format: HH:MM:SS,mmm
        time_str = time_str.replace(",", ".")
        parts = time_str.split(":")
        
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = float(parts[2])
        
        return hours * 3600 + minutes * 60 + seconds
