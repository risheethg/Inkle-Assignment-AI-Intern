"""
AI Client - Wrapper for OpenAI and Anthropic APIs
Provides a unified interface for both providers
"""
from typing import List, Dict, Any
from app.core.config import settings
from app.core.logger import logs
import inspect

class AIClient:
    def __init__(self):
        self.provider = settings.AI_PROVIDER.lower()
        
        if self.provider == "openai":
            from openai import AsyncOpenAI
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not set in environment variables")
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            self.model = settings.OPENAI_MODEL
        elif self.provider == "anthropic":
            from anthropic import AsyncAnthropic
            if not settings.ANTHROPIC_API_KEY:
                raise ValueError("ANTHROPIC_API_KEY not set in environment variables")
            self.client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
            self.model = settings.ANTHROPIC_MODEL
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")
    
    async def chat_completion(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """
        Send a chat completion request to the AI provider
        Returns the assistant's response as a string
        """
        try:
            if self.provider == "openai":
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature
                )
                return response.choices[0].message.content
            
            elif self.provider == "anthropic":
                # Anthropic uses different format - extract system message if present
                system_message = None
                anthropic_messages = []
                
                for msg in messages:
                    if msg["role"] == "system":
                        system_message = msg["content"]
                    else:
                        anthropic_messages.append({
                            "role": msg["role"],
                            "content": msg["content"]
                        })
                
                response = await self.client.messages.create(
                    model=self.model,
                    max_tokens=1024,
                    temperature=temperature,
                    system=system_message if system_message else "",
                    messages=anthropic_messages
                )
                return response.content[0].text
        
        except Exception as e:
            logs.define_logger(
                level=40,
                message=f"Error in AI chat completion: {str(e)}",
                loggName=inspect.stack()[0]
            )
            raise

# Singleton instance
ai_client = AIClient()
