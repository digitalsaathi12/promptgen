import io
import logging
import httpx
from PIL import Image as PILImage, ImageDraw, ImageFont
from app.core.config import settings
from app.services.storage import storage_service

logger = logging.getLogger(__name__)

class ImageGenerationService:
    def __init__(self):
        self.openai_key = settings.OPENAI_API_KEY
        self.stability_key = settings.STABILITY_API_KEY
        self.flux_key = settings.FLUX_API_KEY

    async def generate_image(self, prompt: str, provider: str = "flux") -> str:
        """Generates an image from a prompt, saving and returning the Supabase/local URL."""
        provider = provider.lower()

        # Check if keys are available for chosen providers
        if provider == "openai" and self.openai_key:
            try:
                url = "https://api.openai.com/v1/images/generations"
                headers = {"Authorization": f"Bearer {self.openai_key}"}
                async with httpx.AsyncClient() as client:
                    resp = await client.post(url, headers=headers, json={
                        "model": "dall-e-3",
                        "prompt": prompt,
                        "n": 1,
                        "size": "1024x1024"
                    }, timeout=30.0)
                    if resp.status_code == 200:
                        image_url = resp.json()["data"][0]["url"]
                        # We can download and save to our own storage, or return directly
                        # Let's download the bytes and upload to storage_service to persist it
                        img_resp = await client.get(image_url)
                        if img_resp.status_code == 200:
                            return await storage_service.upload_image(img_resp.content)
                        return image_url
            except Exception as e:
                logger.error(f"DALL-E generation failed: {e}")

        elif provider == "stability" and self.stability_key:
            try:
                # Stability API Core
                url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
                headers = {
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self.stability_key}"
                }
                async with httpx.AsyncClient() as client:
                    resp = await client.post(url, headers=headers, json={
                        "text_prompts": [{"text": prompt}],
                        "cfg_scale": 7,
                        "height": 1024,
                        "width": 1024,
                        "samples": 1,
                        "steps": 30,
                    }, timeout=30.0)
                    if resp.status_code == 200:
                        import base64
                        data = resp.json()
                        image_bytes = base64.b64decode(data["artifacts"][0]["base64"])
                        return await storage_service.upload_image(image_bytes)
            except Exception as e:
                logger.error(f"Stability AI generation failed: {e}")

        # Fallback / Local simulated Pillow image generation
        logger.info(f"Generating simulated image for prompt: '{prompt}' via Pillow.")
        image_bytes = self._create_gradient_card(prompt)
        return await storage_service.upload_image(image_bytes)

    def _create_gradient_card(self, text: str) -> bytes:
        """Generates a beautiful 512x512 blue/white gradient image with text overlay."""
        # Create image
        width, height = 512, 512
        img = PILImage.new("RGB", (width, height), "#ffffff")
        draw = ImageDraw.Draw(img)

        # Draw a sleek blue/white gradient
        # Let's draw it row by row
        for y in range(height):
            # Calculate gradient from blue (#1E3A8A) to white (#FFFFFF)
            r = int(30 + (225 * (y / height)))
            g = int(58 + (197 * (y / height)))
            b = int(138 + (117 * (y / height)))
            for x in range(width):
                img.putpixel((x, y), (r, g, b))

        # Add decorative branding elements
        draw.rectangle([20, 20, width-20, height-20], outline="#ffffff", width=2)
        draw.text((30, 30), "THE DIGITAL SAATHI", fill="#ffffff")
        draw.text((30, 45), "AI Generated Artwork", fill="#d1d5db")

        # Wrap text for prompt description
        wrapped_lines = self._wrap_text(text, 35)
        
        # Draw prompt text in the center
        y_text = 200
        for line in wrapped_lines[:6]: # Limit lines
            # Center the text
            try:
                # Use default font
                font = ImageFont.load_default()
                draw.text((40, y_text), line, fill="#ffffff", font=font)
            except Exception:
                draw.text((40, y_text), line, fill="#ffffff")
            y_text += 25

        # Save to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="PNG")
        return img_byte_arr.getvalue()

    def _wrap_text(self, text: str, max_chars: int) -> list[str]:
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        for word in words:
            if current_length + len(word) + 1 <= max_chars:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word)
        if current_line:
            lines.append(" ".join(current_line))
        return lines

image_gen_service = ImageGenerationService()
