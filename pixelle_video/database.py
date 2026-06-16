"""
Pixelle-Video Database Integration

Handles all database operations for video projects.
"""

import os
import json
from typing import Optional, Dict, Any, List
from datetime import datetime
from pathlib import Path

import asyncpg
from loguru import logger


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://creatorhub:creatorhub123@postgres:5432/creatorhub"
)

SERVICE_NAME = "pixelle-video"


class VideoDatabase:
    """Database operations for Pixelle-Video"""
    
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None
    
    async def connect(self):
        """Connect to database"""
        try:
            self.pool = await asyncpg.create_pool(
                DATABASE_URL,
                min_size=2,
                max_size=10
            )
            logger.info(f"[{SERVICE_NAME}] Database connected")
        except Exception as e:
            logger.error(f"[{SERVICE_NAME}] Database connection failed: {e}")
    
    async def disconnect(self):
        """Disconnect from database"""
        if self.pool:
            await self.pool.close()
    
    # ==================== Video Projects ====================
    
    async def create_project(
        self,
        workspace_id: str,
        name: str,
        topic: str = "",
        script: Dict = None,
        settings: Dict = None
    ) -> Dict:
        """Create a video project"""
        query = """
            INSERT INTO video_projects (workspace_id, name, topic, script, settings)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING *
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                query, workspace_id, name, topic,
                json.dumps(script or {}), json.dumps(settings or {})
            )
        return dict(row)
    
    async def get_project(self, project_id: str) -> Optional[Dict]:
        """Get a video project"""
        query = "SELECT * FROM video_projects WHERE id = $1"
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, project_id)
        return dict(row) if row else None
    
    async def list_projects(self, workspace_id: str) -> List[Dict]:
        """List all video projects in workspace"""
        query = """
            SELECT * FROM video_projects
            WHERE workspace_id = $1
            ORDER BY created_at DESC
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, workspace_id)
        return [dict(row) for row in rows]
    
    async def update_project(
        self,
        project_id: str,
        name: str = None,
        topic: str = None,
        script: Dict = None,
        status: str = None,
        output_path: str = None,
        duration: float = None
    ) -> bool:
        """Update a video project"""
        updates = []
        params = []
        param_count = 0
        
        if name is not None:
            param_count += 1
            updates.append(f"name = ${param_count}")
            params.append(name)
        
        if topic is not None:
            param_count += 1
            updates.append(f"topic = ${param_count}")
            params.append(topic)
        
        if script is not None:
            param_count += 1
            updates.append(f"script = ${param_count}")
            params.append(json.dumps(script))
        
        if status is not None:
            param_count += 1
            updates.append(f"status = ${param_count}")
            params.append(status)
        
        if output_path is not None:
            param_count += 1
            updates.append(f"output_path = ${param_count}")
            params.append(output_path)
        
        if duration is not None:
            param_count += 1
            updates.append(f"duration = ${param_count}")
            params.append(duration)
        
        if not updates:
            return False
        
        param_count += 1
        params.append(project_id)
        
        query = f"""
            UPDATE video_projects
            SET {', '.join(updates)}
            WHERE id = ${param_count}
        """
        
        async with self.pool.acquire() as conn:
            result = await conn.execute(query, *params)
        return result == "UPDATE 1"
    
    async def delete_project(self, project_id: str) -> bool:
        """Delete a video project"""
        query = "DELETE FROM video_projects WHERE id = $1"
        async with self.pool.acquire() as conn:
            result = await conn.execute(query, project_id)
        return result == "DELETE 1"
    
    # ==================== Tasks ====================
    
    async def create_task(
        self,
        project_id: str,
        task_type: str,
        input_data: Dict = None
    ) -> Dict:
        """Create a video task"""
        query = """
            INSERT INTO video_tasks (project_id, task_type, input)
            VALUES ($1, $2, $3)
            RETURNING *
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, project_id, task_type, json.dumps(input_data or {}))
        return dict(row)
    
    async def update_task(
        self,
        task_id: str,
        status: str = None,
        output: Dict = None,
        error: str = None
    ) -> bool:
        """Update a video task"""
        updates = []
        params = []
        param_count = 0
        
        if status is not None:
            param_count += 1
            updates.append(f"status = ${param_count}")
            params.append(status)
            
            if status == "running":
                updates.append("started_at = CURRENT_TIMESTAMP")
            elif status in ("completed", "failed"):
                updates.append("completed_at = CURRENT_TIMESTAMP")
        
        if output is not None:
            param_count += 1
            updates.append(f"output = ${param_count}")
            params.append(json.dumps(output))
        
        if error is not None:
            param_count += 1
            updates.append(f"error = ${param_count}")
            params.append(error)
        
        if not updates:
            return False
        
        param_count += 1
        params.append(task_id)
        
        query = f"""
            UPDATE video_tasks
            SET {', '.join(updates)}
            WHERE id = ${param_count}
        """
        
        async with self.pool.acquire() as conn:
            result = await conn.execute(query, *params)
        return result == "UPDATE 1"
    
    async def get_tasks(self, project_id: str) -> List[Dict]:
        """Get tasks for a project"""
        query = """
            SELECT * FROM video_tasks
            WHERE project_id = $1
            ORDER BY created_at DESC
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, project_id)
        return [dict(row) for row in rows]
    
    # ==================== TTS ====================
    
    async def save_tts(
        self,
        project_id: str,
        engine: str,
        text: str,
        voice: str,
        audio_path: str,
        duration: float = 0,
        settings: Dict = None
    ) -> Dict:
        """Save TTS generation"""
        query = """
            INSERT INTO tts_generations (project_id, engine, text, voice, audio_path, duration, settings)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING *
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                query, project_id, engine, text, voice,
                audio_path, duration, json.dumps(settings or {})
            )
        return dict(row)
    
    async def get_tts(self, project_id: str) -> List[Dict]:
        """Get TTS generations for a project"""
        query = """
            SELECT * FROM tts_generations
            WHERE project_id = $1
            ORDER BY created_at DESC
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, project_id)
        return [dict(row) for row in rows]
    
    # ==================== Subtitles ====================
    
    async def save_subtitle(
        self,
        project_id: str,
        video_path: str,
        language: str,
        segments: List[Dict],
        srt_path: str
    ) -> Dict:
        """Save subtitle generation"""
        query = """
            INSERT INTO subtitle_generations (project_id, video_path, language, segments, srt_path)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING *
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                query, project_id, video_path, language,
                json.dumps(segments), srt_path
            )
        return dict(row)
    
    async def get_subtitles(self, project_id: str) -> List[Dict]:
        """Get subtitles for a project"""
        query = """
            SELECT * FROM subtitle_generations
            WHERE project_id = $1
            ORDER BY created_at DESC
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, project_id)
        return [dict(row) for row in rows]
    
    # ==================== Files ====================
    
    async def register_file(
        self,
        workspace_id: str,
        file_type: str,
        file_path: str,
        metadata: Dict = None
    ) -> Dict:
        """Register a file"""
        file_path_obj = Path(file_path)
        
        query = """
            INSERT INTO files (workspace_id, service, file_type, file_name, file_path, file_size, metadata)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING *
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                query, workspace_id, SERVICE_NAME, file_type,
                file_path_obj.name, file_path,
                file_path_obj.stat().st_size if file_path_obj.exists() else 0,
                json.dumps(metadata or {})
            )
        return dict(row)
    
    async def get_files(
        self,
        workspace_id: str,
        file_type: str = None
    ) -> List[Dict]:
        """Get files"""
        conditions = ["workspace_id = $1", "service = $2"]
        params = [workspace_id, SERVICE_NAME]
        param_count = 2
        
        if file_type:
            param_count += 1
            conditions.append(f"file_type = ${param_count}")
            params.append(file_type)
        
        query = f"""
            SELECT * FROM files
            WHERE {' AND '.join(conditions)}
            ORDER BY created_at DESC
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *params)
        return [dict(row) for row in rows]
    
    # ==================== Logging ====================
    
    async def log_activity(
        self,
        workspace_id: str,
        action: str,
        resource_type: str = None,
        resource_id: str = None,
        details: Dict = None
    ) -> None:
        """Log an activity"""
        query = """
            INSERT INTO activity_logs (workspace_id, service, action, resource_type, resource_id, details)
            VALUES ($1, $2, $3, $4, $5, $6)
        """
        async with self.pool.acquire() as conn:
            await conn.execute(
                query, workspace_id, SERVICE_NAME, action,
                resource_type, resource_id, json.dumps(details or {})
            )


# Global instance
db = VideoDatabase()
