import re
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

# Basic Hindi unicode range check
HINDI_CHAR_REGEX = re.compile(r"[\u0900-\u097f]+")

class OptimizationLayer:
    def normalize_input(self, text: str) -> str:
        """Light cleanup of spaces, capitalization, and punctuation."""
        if not text:
            return ""
        # Clean trailing spaces
        text = text.strip()
        # Clean double spaces
        text = re.sub(r"\s+", " ", text)
        return text

    def detect_language(self, text: str) -> str:
        """Heuristic to detect language from input string (Hinglish vs Hindi vs English)."""
        if not text:
            return "English"
            
        if HINDI_CHAR_REGEX.search(text):
            return "Hindi"
            
        # Hinglish indicators in text (common phonetic Hindi words in Latin characters)
        hinglish_words = {"keliye", "banana", "banana hai", "kaise", "kare", "hai", "ko", "se", "aur", "hota"}
        words = set(text.lower().split())
        if words.intersection(hinglish_words):
            return "Hinglish"
            
        return "English"

    def get_hidden_instructions(self, variables: Dict[str, Any]) -> List[str]:
        """Bakes in background instructions based on parameters (language, tone, platform)."""
        instructions = []
        
        # 1. Language Rules
        lang = str(variables.get("language", "English")).lower()
        if lang in ["hindi", "hi"]:
            instructions.append("CRITICAL: The output must be written entirely in clear, grammatically correct Hindi using the Devanagari script.")
        elif lang in ["hinglish", "hindi-english"]:
            instructions.append(
                "CRITICAL: The output must be written in Hinglish (mixed Hindi + English written in the Latin alphabet). "
                "Use English alphabets to write Hindi words (e.g. 'ye product bohot acha hai'). "
                "Keep the sentence structures natural, modern, and casual, similar to Indian social media chats."
            )
        else:
            instructions.append("Write the output in high-quality English.")

        # 2. Platform Instructions
        platform = str(variables.get("platform", "")).lower()
        if "instagram" in platform or "reel" in platform:
            instructions.append("Optimize for Instagram: Keep sections extremely punchy. Use linebreaks. Append 3-5 trending hashtags.")
        elif "youtube" in platform:
            instructions.append("Optimize for YouTube: Focus on viewer retention. Visual hooks should be sharp and conversational.")
        elif "facebook" in platform:
            instructions.append("Optimize for Facebook: Structure for community shares. Use call-to-actions that drive comments.")

        # 3. Tone settings
        tone = str(variables.get("tone", "")).lower()
        if tone == "casual":
            instructions.append("Keep the tone friendly, conversational, and energetic.")
        elif tone == "professional":
            instructions.append("Maintain an authoritative, clear, and professional tone.")
        elif tone == "funny":
            instructions.append("Incorporate subtle, clean humor where appropriate.")

        return instructions

    def apply_optimizations(self, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Cleans variables and injects the dynamic hidden instructions."""
        optimized_vars = variables.copy()
        
        # Normalize text input payloads
        for key, val in optimized_vars.items():
            if isinstance(val, str):
                optimized_vars[key] = self.normalize_input(val)

        # Detect language dynamically if not specified
        if "language" not in optimized_vars or not optimized_vars["language"]:
            # Check main text variables like 'purpose' or 'topic'
            sample_text = optimized_vars.get("purpose", "") or optimized_vars.get("topic", "") or ""
            optimized_vars["language"] = self.detect_language(sample_text)

        # Retrieve and merge instructions
        hidden_instructions = self.get_hidden_instructions(optimized_vars)
        optimized_vars["hidden_instructions"] = hidden_instructions
        
        return optimized_vars

optimization_layer = OptimizationLayer()
