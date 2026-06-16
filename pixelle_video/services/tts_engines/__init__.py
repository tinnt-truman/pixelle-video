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
TTS Engine Abstraction Layer

Supports multiple TTS engines:
- edge_tts: Microsoft Edge TTS (free, fast)
- azure_tts: Azure Cognitive Services (high quality)
- doubao_tts: ByteDance Doubao TTS (Chinese optimized)
- index_tts: IndexTTS (voice cloning)
"""

from .base import BaseTTSEngine, TTSResult
from .edge_engine import EdgeTTSEngine
from .doubao_engine import DoubaoTTSEngine
from .azure_engine import AzureTTSEngine
from .index_engine import IndexTTSEngine
from .factory import create_tts_engine, get_available_engines

__all__ = [
    "BaseTTSEngine",
    "TTSResult",
    "EdgeTTSEngine",
    "DoubaoTTSEngine",
    "AzureTTSEngine",
    "IndexTTSEngine",
    "create_tts_engine",
    "get_available_engines",
]
