import logging
import httpx
from typing import Dict, Any, List
from app.core.config import settings

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.openai_key = settings.OPENAI_API_KEY
        self.gemini_key = settings.GEMINI_API_KEY
        self.claude_key = settings.CLAUDE_API_KEY
        self.ollama_url = settings.OLLAMA_API_URL

    async def generate_prompt(self, user_input: str) -> Dict[str, str]:
        """Converts Hindi/English text into tailored advanced prompts for GPT, Gemini, and Claude."""
        # Check if keys exist, else return rich mock response
        if not self.openai_key and not self.gemini_key and not self.claude_key:
            return self._simulate_prompt_generation(user_input)

        # Implementation for real API requests using one of the keys (e.g. OpenAI or Gemini)
        try:
            # We'll call the available LLM (defaulting to Gemini or OpenAI) to format this
            prompt_instructions = (
                f"Convert the following description into three advanced AI prompts. "
                f"1. An advanced ChatGPT prompt. 2. An advanced Gemini prompt. 3. An advanced Claude prompt. "
                f"Description: '{user_input}'. "
                f"Return a JSON object with keys: chatgpt_prompt, gemini_prompt, claude_prompt."
            )
            # Example using Gemini API if configured
            if self.gemini_key:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.gemini_key}"
                async with httpx.AsyncClient() as client:
                    resp = await client.post(url, json={
                        "contents": [{"parts": [{"text": prompt_instructions}]}]
                    }, timeout=10.0)
                    if resp.status_code == 200:
                        text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
                        # Extract JSON (simplified parse)
                        return self._parse_json_from_llm(text)
            
            # OpenAI fallback
            if self.openai_key:
                url = "https://api.openai.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.openai_key}"}
                async with httpx.AsyncClient() as client:
                    resp = await client.post(url, headers=headers, json={
                        "model": "gpt-4o-mini",
                        "messages": [{"role": "user", "content": prompt_instructions}],
                        "response_format": {"type": "json_object"}
                    }, timeout=10.0)
                    if resp.status_code == 200:
                        import json
                        content = resp.json()["choices"][0]["message"]["content"]
                        return json.loads(content)

        except Exception as e:
            logger.error(f"Error during AI prompt generation call: {e}. Falling back to simulation.")
            
        return self._simulate_prompt_generation(user_input)

    async def generate_script(self, topic: str, platform: str = "reels") -> Dict[str, str]:
        """Generates visual scripts containing hook, intro, body, and CTA."""
        if not self.openai_key and not self.gemini_key:
            return self._simulate_script_generation(topic, platform)

        try:
            # Call OpenAI if available
            if self.openai_key:
                url = "https://api.openai.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.openai_key}"}
                prompt = (
                    f"Generate a {platform} video script about: '{topic}'. "
                    f"Format the output strictly as a JSON object with keys: 'hook', 'intro', 'body', 'cta'."
                )
                async with httpx.AsyncClient() as client:
                    resp = await client.post(url, headers=headers, json={
                        "model": "gpt-4o-mini",
                        "messages": [{"role": "user", "content": prompt}],
                        "response_format": {"type": "json_object"}
                    }, timeout=10.0)
                    if resp.status_code == 200:
                        import json
                        return json.loads(resp.json()["choices"][0]["message"]["content"])
        except Exception as e:
            logger.error(f"Error during AI script call: {e}")

        return self._simulate_script_generation(topic, platform)

    async def generate_viral_hooks(self, topic: str) -> List[str]:
        """Generates 10 viral hooks of different types."""
        if not self.openai_key:
            return self._simulate_viral_hooks(topic)

        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {self.openai_key}"}
            prompt = (
                f"Generate exactly 10 extremely viral hooks for video about: '{topic}'. "
                f"Provide a mix of Curiosity, Pain, Question, Shock, and Story. "
                f"Return as a JSON list of strings under key 'hooks'."
            )
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, headers=headers, json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": prompt}],
                    "response_format": {"type": "json_object"}
                }, timeout=10.0)
                if resp.status_code == 200:
                    import json
                    res = json.loads(resp.json()["choices"][0]["message"]["content"])
                    return res.get("hooks", [])
        except Exception as e:
            logger.error(f"Error generating hooks: {e}")

        return self._simulate_viral_hooks(topic)

    async def generate_image_prompts(self, input_text: str) -> Dict[str, str]:
        """Generates image prompts for Midjourney, DALL-E, Leonardo, and Stable Diffusion."""
        if not self.openai_key:
            return self._simulate_image_prompts(input_text)

        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {self.openai_key}"}
            prompt = (
                f"Translate this idea: '{input_text}' into four highly descriptive image generation prompts. "
                f"Generate for: 'midjourney', 'dalle', 'leonardo', 'stable_diffusion'. "
                f"Return as a JSON object with keys: 'midjourney', 'dalle', 'leonardo', 'stable_diffusion'."
            )
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, headers=headers, json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": prompt}],
                    "response_format": {"type": "json_object"}
                }, timeout=10.0)
                if resp.status_code == 200:
                    import json
                    return json.loads(resp.json()["choices"][0]["message"]["content"])
        except Exception as e:
            logger.error(f"Error generating image prompts: {e}")

        return self._simulate_image_prompts(input_text)

    async def chat_message(self, message: str, provider: str = "gpt", history: List[Dict[str, str]] = None) -> str:
        """Runs conversational chats with specific AI engines (GPT, Gemini, Claude, Ollama)."""
        provider = provider.lower()
        
        # Format the system prompt to reflect the Digital Saathi identity
        system_content = "You are Digital Saathi (डिजिटल साथी), a helpful AI assistant supporting English and Hindi."
        messages = [{"role": "system", "content": system_content}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": message})

        # OpenAI Call
        if provider in ["gpt", "openai"] and self.openai_key:
            try:
                url = "https://api.openai.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.openai_key}"}
                async with httpx.AsyncClient() as client:
                    resp = await client.post(url, headers=headers, json={
                        "model": "gpt-4o-mini",
                        "messages": messages
                    }, timeout=15.0)
                    if resp.status_code == 200:
                        return resp.json()["choices"][0]["message"]["content"]
            except Exception as e:
                logger.error(f"OpenAI Chat failed: {e}")

        # Gemini Call
        if provider == "gemini" and self.gemini_key:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.gemini_key}"
                # Map simple format to Gemini contents schema
                contents = []
                for msg in messages:
                    if msg["role"] == "system":
                        # Gemini supports system instruction differently, but for simplicity we append as role 'user' / 'model'
                        continue
                    role = "user" if msg["role"] == "user" else "model"
                    contents.append({"role": role, "parts": [{"text": msg["content"]}]})
                
                async with httpx.AsyncClient() as client:
                    resp = await client.post(url, json={"contents": contents}, timeout=15.0)
                    if resp.status_code == 200:
                        return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
            except Exception as e:
                logger.error(f"Gemini Chat failed: {e}")

        # Claude Call
        if provider == "claude" and self.claude_key:
            try:
                url = "https://api.anthropic.com/v1/messages"
                headers = {
                    "x-api-key": self.claude_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                }
                # Filter out system message and set as param
                user_messages = [m for m in messages if m["role"] != "system"]
                async with httpx.AsyncClient() as client:
                    resp = await client.post(url, headers=headers, json={
                        "model": "claude-3-haiku-20240307",
                        "max_tokens": 1024,
                        "messages": [{"role": m["role"], "content": m["content"]} for m in user_messages],
                        "system": system_content
                    }, timeout=15.0)
                    if resp.status_code == 200:
                        return resp.json()["content"][0]["text"]
            except Exception as e:
                logger.error(f"Claude Chat failed: {e}")

        # Ollama Call
        if provider == "ollama":
            try:
                url = f"{self.ollama_url}/api/chat"
                async with httpx.AsyncClient() as client:
                    resp = await client.post(url, json={
                        "model": "llama3",
                        "messages": messages,
                        "stream": False
                    }, timeout=10.0)
                    if resp.status_code == 200:
                        return resp.json()["message"]["content"]
            except Exception as e:
                logger.error(f"Ollama chat connection failed: {e}")

        # Return a simulated conversation response
        return self._simulate_chat_response(message, provider)

    # --- Simulated fallbacks for local run without keys ---

    def _simulate_prompt_generation(self, user_input: str) -> Dict[str, str]:
        # Translates mixed English/Hindi request into structured prompts
        is_hindi = any(c in user_input for c in ["है", "के", "लिए", "बनाना", "करना"]) or "keliye" in user_input.lower()
        topic = user_input if not is_hindi else "the requested campaign in Hindi/English context"
        
        return {
            "chatgpt_prompt": (
                f"Act as a professional copywriter and marketing strategist. I need to write an advertisement for: '{topic}'. "
                f"Develop a high-converting landing page script and short ad copy. Focus on benefits, user pain points, "
                f"and provide 3 variants of CTR buttons. Output the content with clear section headers."
            ),
            "gemini_prompt": (
                f"Analyze the market demands for: '{topic}'. Create a structured blueprint for a marketing campaign. "
                f"Outline the Target Audience personas, the value proposition, and compose a 30-second video script "
                f"with visual cues. Maintain a friendly and engaging tone."
            ),
            "claude_prompt": (
                f"Context: '{topic}'. I want you to perform a deep positioning analysis. Who are the primary audience segments? "
                f"Draft a detailed narrative strategy, list key hooks, and compile a list of FAQs that resolve primary "
                f"conversion blocks. Keep the tone sophisticated, direct, and outcome-oriented."
            )
        }

    def _simulate_script_generation(self, topic: str, platform: str) -> Dict[str, str]:
        return {
            "hook": f"🛑 Stop scrolling! If you care about {topic}, you need to watch this right now.",
            "intro": f"Hey guys! Today we are talking about {topic}. Most people get this completely wrong, but here is the secret.",
            "body": f"First, establish clear goals for {topic}. Second, optimize your strategy using automated systems. Finally, track and analyze your weekly results.",
            "cta": f"Want to master {topic}? Hit that follow button and check the link in our bio for a free guide!"
        }

    def _simulate_viral_hooks(self, topic: str) -> List[str]:
        return [
            f"Why 99% of people fail at {topic} (and how to fix it).",
            f"The dark truth about {topic} that nobody wants to talk about.",
            f"If you do this one thing, your {topic} results will double overnight.",
            f"How I went from 0 to master of {topic} in exactly 14 days.",
            f"Stop doing this with {topic} - it's costing you thousands of dollars!",
            f"What experts aren't telling you about {topic}.",
            f"This simple {topic} trick feels illegal to know.",
            f"My secret system for {topic} that generated millions of views.",
            f"Are you making this critical mistake with {topic}?",
            f"Here is the easiest way to succeed with {topic} in 2026."
        ]

    def _simulate_image_prompts(self, input_text: str) -> Dict[str, str]:
        return {
            "midjourney": f"An ultra-realistic, highly detailed cinematic poster of '{input_text}', volumetric lighting, 8k resolution, photorealistic, cinematic composition --ar 16:9 --v 6.0",
            "dalle": f"A vibrant and detailed illustration depicting '{input_text}', digital art style, volumetric light rays, concept art, trending on ArtStation.",
            "leonardo": f"Masterpiece of '{input_text}', fantasy art, intricate details, gorgeous color grading, dramatic shadows, octane render.",
            "stable_diffusion": f"Hyperrealistic photo of '{input_text}', studio lighting, sharp focus, professional camera shot, award-winning photography."
        }

    def _simulate_chat_response(self, message: str, provider: str) -> str:
        # Detect simple Hindi tokens and greet in Hindi
        if any(w in message.lower() for w in ["hello", "hi", "नमस्ते", "namaste", "hey"]):
            return (
                f"नमस्ते! मैं आपका डिजिटल साथी हूँ। (Resolved via simulated {provider.upper()})\n\n"
                f"Hello! I am your Digital Saathi. How can I assist you with your marketing, content, or prompt generation today?"
            )
        return (
            f"Sure! I can help you with that. Regarding your query: '{message}'.\n\n"
            f"Here is a comprehensive breakdown. We should build a structured approach around this topic, optimize for readability, "
            f"and target key customer touchpoints.\n\n"
            f"Is there anything specific you'd like to refine? (Response simulated via {provider.upper()})"
        )

    def _parse_json_from_llm(self, text: str) -> Dict[str, str]:
        # Helper to extract JSON from LLM markdown code blocks
        import json
        try:
            # Remove markdown backticks if present
            cleaned = text.strip()
            if cleaned.startswith("```"):
                lines = cleaned.splitlines()
                if lines[0].startswith("```json") or lines[0] == "```":
                    cleaned = "\n".join(lines[1:-1])
            return json.loads(cleaned)
        except Exception:
            # Fallback parsing regex or return user input
            return {"chatgpt_prompt": text, "gemini_prompt": text, "claude_prompt": text}

ai_service = AIService()
