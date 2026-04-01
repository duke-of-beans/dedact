"""
Checkpoint Manager Module
Save and restore processing state
"""

from pathlib import Path
from typing import Dict, Optional
import json
from datetime import datetime


class CheckpointManager:
    """
    Manage processing checkpoints
    
    Features:
    - Save processing state
    - Resume from checkpoint
    - Automatic cleanup
    """
    
    def __init__(self, checkpoint_dir: Path = Path('checkpoints')):
        """
        Initialize checkpoint manager
        
        Args:
            checkpoint_dir: Directory for checkpoint files
        """
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
    
    def save_checkpoint(
        self,
        checkpoint_id: str,
        state: Dict
    ) -> Path:
        """
        Save checkpoint
        
        Args:
            checkpoint_id: Unique checkpoint identifier
            state: Processing state to save
            
        Returns:
            Path to checkpoint file
        """
        checkpoint_path = self.checkpoint_dir / f"{checkpoint_id}.json"
        
        checkpoint_data = {
            'checkpoint_id': checkpoint_id,
            'timestamp': datetime.now().isoformat(),
            'state': state
        }
        
        with open(checkpoint_path, 'w') as f:
            json.dump(checkpoint_data, f, indent=2, default=str)
        
        return checkpoint_path
    
    def load_checkpoint(self, checkpoint_id: str) -> Optional[Dict]:
        """
        Load checkpoint
        
        Args:
            checkpoint_id: Checkpoint identifier
            
        Returns:
            Checkpoint state or None if not found
        """
        checkpoint_path = self.checkpoint_dir / f"{checkpoint_id}.json"
        
        if not checkpoint_path.exists():
            return None
        
        with open(checkpoint_path, 'r') as f:
            checkpoint_data = json.load(f)
        
        return checkpoint_data.get('state')
    
    def list_checkpoints(self) -> list:
        """List all available checkpoints"""
        checkpoints = []
        for file in self.checkpoint_dir.glob('*.json'):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    checkpoints.append({
                        'id': data.get('checkpoint_id'),
                        'timestamp': data.get('timestamp'),
                        'file': str(file)
                    })
            except:
                pass
        return sorted(checkpoints, key=lambda x: x['timestamp'], reverse=True)
    
    def delete_checkpoint(self, checkpoint_id: str) -> bool:
        """Delete checkpoint file"""
        checkpoint_path = self.checkpoint_dir / f"{checkpoint_id}.json"
        if checkpoint_path.exists():
            checkpoint_path.unlink()
            return True
        return False
