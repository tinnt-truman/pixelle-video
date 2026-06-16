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
TTS Engine Factory

Creates and manages TTS engine instances.
"""

from typing import Dict, List, Optional

from loguru import logger

from .base import BaseTTSEngine
from .edge_engine import EdgeTTSEngine
from .doubao_engine import DoubaoTTSEngine
from .azure_engine import AzureTTSEngine
from .index_engine import IndexTTSEngine


# Engine registry
ENGINES = {
    "edge_tts": EdgeTTSEngine,
    "doubao_tts": DoubaoTTSEngine,
    "azure_tts": AzureTTSEngine,
    "index_tts": IndexTTSEngine,
}

# Global engine instances
_engine_instances: Dict[str, BaseTTSEngine] = {}


def create_tts_engine(
    engine_name: str,
    config: dict = None
) -> BaseTTSEngine:
    """
    Create a TTS engine instance
    
    Args:
        engine_name: Name of the engine ("edge_tts", "doubao_tts", etc.)
        config: Engine-specific configuration
    
    Returns:
        TTS engine instance
    
    Raises:
        ValueError: If engine not found
    """
    if engine_name not in ENGINES:
        raise ValueError(
            f"Unknown TTS engine: {engine_name}. "
            f"Available engines: {list(ENGINES.keys())}"
        )
    
    # Check cache
    cache_key = f"{engine_name}:{hash(str(config))}"
    if cache_key in _engine_instances:
        return _engine_instances[cache_key]
    
    # Create new instance
    engine_class = ENGINES[engine_name]
    engine = engine_class(config or {})
    
    # Cache
    _engine_instances[cache_key] = engine
    
    logger.info(f"Created TTS engine: {engine_name}")
    return engine


def get_available_engines() -> List[dict]:
    """
    Get list of available TTS engines
    
    Returns:
        List of engine info dicts
    """
    engines = []
    
    for name, engine_class in ENGINES.items():
        try:
            # Try to create with empty config
            engine = engine_class({})
            engines.append({
                "name": name,
                "class": engine_class.__name__,
                "available": engine.is_available()
            })
        except Exception as e:
            engines.append({
                "name": name,
                "class": engine_class.__name__,
                "available": False,
                "error": str(e)
            })
    
    return engines


def get_engine(name: str) -> Optional[BaseTTSEngine]:
    """
    Get cached engine instance
    
    Args:
        name: Engine name
    
    Returns:
        Engine instance or None
    """
    # Find any cached instance with this engine name
    for key, engine in _engine_instances.items():
        if key.startswith(f"{name}:"):
            return engine
    return None
