"""
AI Client - Wrapper for OpenAI, Anthropic, and Google Gemini APIs
Provides a unified interface for all providers
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
        elif self.provider == "gemini":
            import google.generativeai as genai
            if not settings.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY not set in environment variables")
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.genai = genai
            self.model = settings.GEMINI_MODEL
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
            
            elif self.provider == "gemini":
                # Convert messages to a simple prompt for Gemini
                prompt_parts = []
                
                for msg in messages:
                    role = msg["role"]
                    content = msg["content"]
                    if role == "system":
                        prompt_parts.append(f"Instructions: {content}")
                    elif role == "user":
                        prompt_parts.append(f"User: {content}")
                    elif role == "assistant":
                        prompt_parts.append(f"Assistant: {content}")
                
                full_prompt = "\n\n".join(prompt_parts)
                
                # Use generate_content method
                model = self.genai.GenerativeModel(self.model)
                response = model.generate_content(
                    full_prompt,
                    generation_config=self.genai.types.GenerationConfig(
                        temperature=temperature,
                        max_output_tokens=1024,
                    )
                )
                
                # Handle complex responses
                try:
                    return response.text
                except:
                    # If .text fails, manually extract text from parts
                    if response.candidates:
                        parts = response.candidates[0].content.parts
                        return "".join(part.text for part in parts if hasattr(part, 'text'))
                    return ""
        
        except Exception as e:
            logs.define_logger(
                level=40,
                message=f"Error in AI chat completion: {str(e)}",
                loggName=inspect.stack()[0]
            )
            raise

# Singleton instance
ai_client = AIClient()
