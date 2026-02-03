"""
GitGoblin AI Commit Message Generator
Uses Groq API to generate descriptive commit messages
"""

import subprocess
import json
from pathlib import Path


class AICommitGenerator:
    """Generate commit messages using Groq AI"""
    
    def __init__(self, api_key, repo_path='.'):
        self.api_key = api_key
        self.repo_path = Path(repo_path).resolve()
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
    
    def get_git_diff(self, file_path=None):
        """Get git diff for the changes"""
        try:
            if file_path:
                # Get diff for specific file
                result = subprocess.run(
                    ['git', 'diff', '--cached', file_path],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
            else:
                # Get diff for all staged changes
                result = subprocess.run(
                    ['git', 'diff', '--cached'],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
            
            diff = result.stdout.strip()
            
            # If no staged changes, get unstaged diff
            if not diff:
                if file_path:
                    result = subprocess.run(
                        ['git', 'diff', file_path],
                        cwd=self.repo_path,
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                else:
                    result = subprocess.run(
                        ['git', 'diff'],
                        cwd=self.repo_path,
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                diff = result.stdout.strip()
            
            return diff
        except Exception as e:
            print(f"⚠️  Could not get git diff: {e}")
            return ""
    
    def get_file_status(self, file_path=None):
        """Get status of files"""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain', file_path] if file_path else ['git', 'status', '--porcelain'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip()
        except Exception as e:
            print(f"⚠️  Could not get git status: {e}")
            return ""
    
    def generate_commit_message(self, file_path=None):
        """Generate a descriptive commit message using Groq AI"""
        try:
            # Get git diff
            diff = self.get_git_diff(file_path)
            status = self.get_file_status(file_path)
            
            if not diff and not status:
                return None
            
            # Prepare the prompt for Groq
            prompt = self._create_prompt(diff, status, file_path)
            
            # Call Groq API
            commit_message = self._call_groq_api(prompt)
            
            return commit_message
            
        except Exception as e:
            print(f"⚠️  AI generation failed: {e}")
            return None
    
    def _create_prompt(self, diff, status, file_path=None):
        """Create a detailed prompt for the AI"""
        prompt = """You are an expert software developer writing git commit messages. 
Generate a clear, descriptive commit message following these rules:

1. Use conventional commits format: <type>: <description>
2. Types: feat, fix, docs, style, refactor, test, chore
3. Keep the first line under 72 characters
4. If changes are complex, add a blank line and detailed bullet points
5. Be specific about what changed and why
6. Focus on the impact and purpose, not just what was done

"""
        
        if file_path:
            prompt += f"\nFile modified: {file_path}\n"
        
        if status:
            prompt += f"\nGit Status:\n{status}\n"
        
        if diff:
            # Limit diff size to avoid token limits
            diff_preview = diff[:3000] if len(diff) > 3000 else diff
            prompt += f"\nGit Diff:\n```\n{diff_preview}\n```\n"
        
        prompt += "\nGenerate ONLY the commit message, no explanations or additional text:"
        
        return prompt
    
    def _call_groq_api(self, prompt):
        """Call Groq API to generate commit message"""
        try:
            import requests
        except ImportError:
            raise ImportError("requests library is required. Install with: pip install requests")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates concise, descriptive git commit messages following conventional commits format."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            
            result = response.json()
            commit_message = result['choices'][0]['message']['content'].strip()
            
            # Clean up the message (remove quotes if present)
            commit_message = commit_message.strip('"').strip("'")
            
            return commit_message
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            raise
        except (KeyError, json.JSONDecodeError) as e:
            print(f"❌ Failed to parse API response: {e}")
            raise
    
    def generate_sneak_commit_message(self):
        """Generate commit message for sneak command (all changes)"""
        return self.generate_commit_message(file_path=None)
