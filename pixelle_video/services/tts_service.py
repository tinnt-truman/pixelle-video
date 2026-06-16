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
TTS (Text-to-Speech) Service - Supports multiple engines and ComfyUI workflows

Engines:
- edge_tts: Microsoft Edge TTS (free, fast, good quality)
- doubao_tts: ByteDance Doubao TTS (Chinese optimized)
- azure_tts: Azure Cognitive Services (enterprise-grade)
- index_tts: IndexTTS (voice cloning)
"""

import os
import uuid
from pathlib import Path
from typing import Optional, List

from comfykit import ComfyKit
from loguru import logger

from pixelle_video.services.comfy_base_service import ComfyBaseService
from pixelle_video.utils.tts_util import edge_tts
from pixelle_video.tts_voices import speed_to_rate
from pixelle_video.services.tts_engines import (
    create_tts_engine,
    get_available_engines,
    TTSResult,
)


class TTSService(ComfyBaseService):
    """
    TTS (Text-to-Speech) service - Multi-engine + Workflow-based
    
    Supports:
    1. Local engines: edge_tts, doubao_tts, azure_tts, index_tts
    2. ComfyUI workflows (via ComfyKit)
    
    Usage:
        # Use local engine (edge_tts by default)
        audio_path = await pixelle_video.tts(text="Hello, world!")
        
        # Use specific engine
        audio_path = await pixelle_video.tts(
            text="Hello!",
            engine="doubao_tts"
        )
        
        # Use ComfyUI workflow
        audio_path = await pixelle_video.tts(
            text="你好，世界！",
            workflow="tts_edge.json"
        )
        
        # List available engines
        engines = pixelle_video.tts.list_engines()
        
        # List available workflows
        workflows = pixelle_video.tts.list_workflows()
    """
    
    WORKFLOW_PREFIX = "tts_"
    DEFAULT_WORKFLOW = None  # No hardcoded default, must be configured
    WORKFLOWS_DIR = "workflows"
    
    def __init__(self, config: dict, core=None):
        """
        Initialize TTS service
        
        Args:
            config: Full application config dict
            core: PixelleVideoCore instance (for accessing shared ComfyKit)
        """
        super().__init__(config, service_name="tts", core=core)
        
        # Engine configurations
        self.engine_configs = config.get("tts_engines", {})
    
    
    async def __call__(
        self,
        text: str,
        workflow: Optional[str] = None,
        # Engine selection
        engine: Optional[str] = None,
        # ComfyUI connection (optional overrides)
        comfyui_url: Optional[str] = None,
        runninghub_api_key: Optional[str] = None,
        # TTS parameters
        voice: Optional[str] = None,
        speed: Optional[float] = None,
        pitch: Optional[float] = None,
        ref_audio: Optional[str] = None,
        # Inference mode override
        inference_mode: Optional[str] = None,
        # Output path
        output_path: Optional[str] = None,
        **params
    ) -> str:
        """
        Generate speech using local engine or ComfyUI workflow
        
        Args:
            text: Text to convert to speech
            workflow: Workflow filename (for ComfyUI mode, default: from config)
            engine: TTS engine name ("edge_tts", "doubao_tts", "azure_tts", "index_tts")
            comfyui_url: ComfyUI URL (optional, overrides config)
            runninghub_api_key: RunningHub API key (optional, overrides config)
            voice: Voice ID (engine-specific)
            speed: Speech speed multiplier (1.0 = normal, >1.0 = faster, <1.0 = slower)
            pitch: Pitch multiplier (1.0 = normal)
            ref_audio: Reference audio path for voice cloning (IndexTTS)
            inference_mode: Override inference mode ("local" or "comfyui", default: from config)
            output_path: Custom output path (auto-generated if None)
            **params: Additional workflow parameters
        
        Returns:
            Generated audio file path
        
        Examples:
            # Edge TTS (default)
            audio_path = await pixelle_video.tts(
                text="Hello, world!",
                voice="vi-VN-HoaiMyNeural",
                speed=1.2
            )
            
            # Doubao TTS
            audio_path = await pixelle_video.tts(
                text="你好，世界！",
                engine="doubao_tts",
                voice="zh_female_shuangkuaisisi_moon_bigtts"
            )
            
            # IndexTTS (voice cloning)
            audio_path = await pixelle_video.tts(
                text="This is cloned voice",
                engine="index_tts",
                ref_audio="path/to/reference.wav"
            )
            
            # ComfyUI workflow
            audio_path = await pixelle_video.tts(
                text="你好，世界！",
                inference_mode="comfyui",
                workflow="runninghub/tts_edge.json"
            )
        """
        # Determine inference mode (param > config)
        mode = inference_mode or self.config.get("inference_mode", "local")
        
        # Route to appropriate implementation
        if mode == "local":
            # Use multi-engine TTS
            return await self._call_engine_tts(
                text=text,
                engine=engine,
                voice=voice,
                speed=speed,
                pitch=pitch,
                ref_audio=ref_audio,
                output_path=output_path
            )
        else:  # comfyui
            # 1. Resolve workflow (returns structured info)
            workflow_info = self._resolve_workflow(workflow=workflow)
            
            # 2. Execute ComfyUI workflow
            return await self._call_comfyui_workflow(
                workflow_info=workflow_info,
                text=text,
                comfyui_url=comfyui_url,
                runninghub_api_key=runninghub_api_key,
                voice=voice,
                speed=speed,
                output_path=output_path,
                **params
            )
    
    def list_engines(self) -> List[dict]:
        """
        List available TTS engines
        
        Returns:
            List of engine info dicts
        """
        return get_available_engines()
    
    async def _call_engine_tts(
        self,
        text: str,
        engine: Optional[str] = None,
        voice: Optional[str] = None,
        speed: Optional[float] = None,
        pitch: Optional[float] = None,
        ref_audio: Optional[str] = None,
        output_path: Optional[str] = None,
    ) -> str:
        """
        Generate speech using multi-engine TTS
        
        Args:
            text: Text to convert to speech
            engine: TTS engine name (default: from config)
            voice: Voice ID (engine-specific)
            speed: Speech speed multiplier (default: from config)
            pitch: Pitch multiplier (default: from config)
            ref_audio: Reference audio path for voice cloning
            output_path: Custom output path
        
        Returns:
            Generated audio file path
        """
        # Determine engine (param > config > default)
        engine_name = engine or self.config.get("default_engine", "edge_tts")
        
        # Get engine config
        engine_config = self.engine_configs.get(engine_name, {})
        
        # Create engine instance
        try:
            tts_engine = create_tts_engine(engine_name, engine_config)
        except Exception as e:
            logger.error(f"Failed to create TTS engine {engine_name}: {e}")
            # Fallback to edge_tts
            tts_engine = create_tts_engine("edge_tts", {})
            engine_name = "edge_tts"
        
        # Get defaults from config
        local_config = self.config.get("local", {})
        final_voice = voice or local_config.get("voice", "vi-VN-HoaiMyNeural")
        final_speed = speed if speed is not None else local_config.get("speed", 1.0)
        final_pitch = pitch if pitch is not None else local_config.get("pitch", 1.0)
        
        logger.info(f"🎙️  Using {engine_name}: voice={final_voice}, speed={final_speed}x")
        
        # Generate output path if not provided
        if not output_path:
            unique_id = uuid.uuid4().hex
            ext = "wav" if engine_name == "index_tts" else "mp3"
            output_path = f"output/tts/{unique_id}.{ext}"
        
        # Synthesize
        try:
            result: TTSResult = await tts_engine.synthesize(
                text=text,
                voice=final_voice,
                speed=final_speed,
                pitch=final_pitch,
                output_path=output_path,
                ref_audio=ref_audio
            )
            
            logger.info(f"✅ Generated audio ({engine_name}): {result.audio_path}")
            return result.audio_path
            
        except Exception as e:
            logger.error(f"TTS generation error ({engine_name}): {e}")
            raise
    
    async def _call_comfyui_workflow(
        self,
        workflow_info: dict,
        text: str,
        comfyui_url: Optional[str] = None,
        runninghub_api_key: Optional[str] = None,
        voice: Optional[str] = None,
        speed: float = 1.0,
        output_path: Optional[str] = None,
        **params
    ) -> str:
        """
        Generate speech using ComfyUI workflow
        
        Args:
            workflow_info: Workflow info dict from _resolve_workflow()
            text: Text to convert to speech
            comfyui_url: ComfyUI URL
            runninghub_api_key: RunningHub API key
            voice: Voice ID (workflow-specific)
            speed: Speech speed multiplier (workflow-specific)
            output_path: Custom output path (downloads if URL returned)
            **params: Additional workflow parameters
        
        Returns:
            Generated audio file path (local if output_path provided, otherwise URL)
        """
        logger.info(f"🎙️  Using workflow: {workflow_info['key']}")
        
        # 1. Build workflow parameters (ComfyKit config is now managed by core)
        workflow_params = {"text": text}
        
        # Add optional TTS parameters (only if explicitly provided and not None)
        if voice is not None:
            workflow_params["voice"] = voice
        if speed is not None and speed != 1.0:
            workflow_params["speed"] = speed
        
        # Add any additional parameters
        workflow_params.update(params)
        
        logger.debug(f"Workflow parameters: {workflow_params}")
        
        # 3. Execute workflow using shared ComfyKit instance from core
        try:
            # Get shared ComfyKit instance (lazy initialization + config hot-reload)
            kit = await self.core._get_or_create_comfykit()
            
            # Determine what to pass to ComfyKit based on source
            if workflow_info["source"] == "runninghub" and "workflow_id" in workflow_info:
                # RunningHub: pass workflow_id
                workflow_input = workflow_info["workflow_id"]
                logger.info(f"Executing RunningHub TTS workflow: {workflow_input}")
            else:
                # Selfhost: pass file path
                workflow_input = workflow_info["path"]
                logger.info(f"Executing selfhost TTS workflow: {workflow_input}")
            
            result = await kit.execute(workflow_input, workflow_params)
            
            # 4. Handle result
            if result.status != "completed":
                error_msg = result.msg or "Unknown error"
                logger.error(f"TTS generation failed: {error_msg}")
                raise Exception(f"TTS generation failed: {error_msg}")
            
            # ComfyKit result can have audio files in different output types
            # Try to get audio file path from result
            audio_path = None
            
            # Check for audio files in result.audios (if available)
            if hasattr(result, 'audios') and result.audios:
                audio_path = result.audios[0]
                logger.debug(f"✅ Found audio in result.audios: {audio_path}")
            # Check for files in result.files
            elif hasattr(result, 'files') and result.files:
                audio_path = result.files[0]
                logger.debug(f"✅ Found audio in result.files: {audio_path}")
            # Check in outputs dictionary
            elif hasattr(result, 'outputs') and result.outputs:
                logger.debug(f"Searching for audio file in result.outputs: {result.outputs}")
                # Try to find audio file in outputs
                for key, value in result.outputs.items():
                    if isinstance(value, str) and any(value.endswith(ext) for ext in ['.mp3', '.wav', '.flac']):
                        audio_path = value
                        logger.debug(f"✅ Found audio in result.outputs[{key}]: {audio_path}")
                        break
            
            if not audio_path:
                logger.error("No audio file generated")
                logger.error(f"❌ Result analysis:")
                logger.error(f"   - result.audios: {getattr(result, 'audios', 'NOT_FOUND')}")
                logger.error(f"   - result.files: {getattr(result, 'files', 'NOT_FOUND')}")
                logger.error(f"   - result.outputs: {getattr(result, 'outputs', 'NOT_FOUND')}")
                logger.error(f"   - Full __dict__: {result.__dict__}")
                raise Exception("No audio file generated by workflow")
            
            # If output_path provided and audio_path is URL, download to local
            if output_path and audio_path.startswith(('http://', 'https://')):
                import httpx
                import os
                
                # Ensure parent directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                logger.info(f"Downloading audio from {audio_path} to {output_path}")
                async with httpx.AsyncClient() as client:
                    response = await client.get(audio_path)
                    response.raise_for_status()
                    
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                
                logger.info(f"✅ Generated audio (ComfyUI): {output_path}")
                return output_path
            
            logger.info(f"✅ Generated audio (ComfyUI): {audio_path}")
            return audio_path
        
        except Exception as e:
            logger.error(f"TTS generation error: {e}")
            raise
