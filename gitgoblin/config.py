"""
GitGoblin Configuration Management
"""

import os
import json
from pathlib import Path


class GoblinConfig:
    """Manage GitGoblin configuration"""
    
    def __init__(self, repo_path='.'):
        self.repo_path = Path(repo_path).resolve()
        self.config_file = self.repo_path / '.git' / 'gitgoblin.config.json'
        self.config = self._load_config()
    
    def _load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Could not load config: {e}")
                return {}
        return {}
    
    def _save_config(self):
        """Save configuration to file"""
        try:
            # Ensure .git directory exists
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"⚠️  Could not save config: {e}")
            return False
    
    def set_api_key(self, api_key):
        """Set Groq API key"""
        self.config['groq_api_key'] = api_key
        # Also set as generic ai_api_key for flexibility
        self.config['ai_api_key'] = api_key
        return self._save_config()
    
    def get_api_key(self):
        """Get AI API key (Groq or legacy DeepSeek)"""
        # First check environment variable for Groq
        env_key = os.getenv('GROQ_API_KEY')
        if env_key:
            return env_key
        
        # Check legacy DeepSeek env var
        env_key = os.getenv('DEEPSEEK_API_KEY')
        if env_key:
            return env_key
        
        # Check config file for Groq key
        groq_key = self.config.get('groq_api_key')
        if groq_key:
            return groq_key
        
        # Check generic AI key
        ai_key = self.config.get('ai_api_key')
        if ai_key:
            return ai_key
        
        # Fallback to legacy DeepSeek key
        return self.config.get('deepseek_api_key')
    
    def enable_ai_commits(self, enabled=True):
        """Enable or disable AI-generated commit messages"""
        self.config['ai_commits_enabled'] = enabled
        return self._save_config()
    
    def is_ai_enabled(self):
        """Check if AI commits are enabled"""
        return self.config.get('ai_commits_enabled', False)
    
    def get_all_config(self):
        """Get all configuration"""
        return self.config.copy()
    
    def set_config(self, key, value):
        """Set a configuration value"""
        self.config[key] = value
        return self._save_config()
    
    def get_config(self, key, default=None):
        """Get a configuration value"""
        return self.config.get(key, default)
