"""Google Gemini 3 Pro Image (Nano Banana Pro) image generation and editing."""

import io
import os
from pathlib import Path
from typing import Optional, Union

import google.genai as genai
from PIL import Image


class NanoBanana:
    """Generate and edit images using Google Gemini 3 Pro Image model."""

    ASPECT_RATIOS = {
        "1:1": (1024, 1024),
        "2:3": (1024, 1536),
        "3:2": (1536, 1024),
        "3:4": (1024, 1365),
        "4:3": (1365, 1024),
        "4:5": (1024, 1280),
        "5:4": (1280, 1024),
        "9:16": (1024, 1820),
        "16:9": (1820, 1024),
        "21:9": (2400, 1028),
    }

    SIZE_DIMENSIONS = {
        "standard": (1024, 1024),
        "2K": (2048, 2048),
        "4K": (3840, 3840),
    }

    def __init__(self, api_key: Optional[str] = None) -> None:
        """Initialize Nano Banana generator.

        Args:
            api_key: Google Gemini API key. If None, reads from GEMINI_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable not set. "
                "Get your API key from https://aistudio.google.com/apikey"
            )

        genai.configure(api_key=self.api_key)
        self.model = genai.ImageGenerationModel("gemini-3-pro-image-preview")

    def generate_image(
        self,
        prompt: str,
        output_path: Optional[Union[str, Path]] = None,
        aspect_ratio: str = "1:1",
        image_size: str = "standard",
        search_grounding: bool = False,
    ) -> Union[Image.Image, Path]:
        """Generate an image from a text prompt.

        Args:
            prompt: Text description of the image to generate.
            output_path: Path to save the generated image. If None, returns PIL Image.
            aspect_ratio: Image aspect ratio (1:1, 16:9, 9:16, 21:9, etc.).
            image_size: Image size (standard, 2K, 4K).
            search_grounding: Enable Google Search grounding for accuracy.

        Returns:
            PIL Image if output_path is None, else Path to saved image.

        Raises:
            ValueError: If aspect_ratio or image_size is invalid.
        """
        if aspect_ratio not in self.ASPECT_RATIOS:
            valid_ratios = ", ".join(self.ASPECT_RATIOS.keys())
            raise ValueError(
                f"Invalid aspect ratio '{aspect_ratio}'. "
                f"Valid options: {valid_ratios}"
            )

        if image_size not in self.SIZE_DIMENSIONS:
            valid_sizes = ", ".join(self.SIZE_DIMENSIONS.keys())
            raise ValueError(
                f"Invalid image size '{image_size}'. "
                f"Valid options: {valid_sizes}"
            )

        # Calculate dimensions based on aspect ratio and size
        base_width, base_height = self.ASPECT_RATIOS[aspect_ratio]
        if image_size in self.SIZE_DIMENSIONS:
            max_dim = max(self.SIZE_DIMENSIONS[image_size])
            max_base = max(base_width, base_height)
            scale = max_dim / max_base
            width = int(base_width * scale)
            height = int(base_height * scale)
        else:
            width, height = base_width, base_height

        # Generate image
        response = self.model.generate_images(
            prompt=prompt,
            number_of_images=1,
            safety_filter_level="block_only_high",
            aspect_ratio=aspect_ratio,
            quality_tier="standard",
        )

        if not response.images:
            raise RuntimeError(f"Failed to generate image for prompt: {prompt}")

        image = response.images[0]

        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            image.save(output_path, format="PNG")
            return output_path

        return image

    def edit_image(
        self,
        prompt: str,
        input_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
        search_grounding: bool = False,
    ) -> Union[Image.Image, Path]:
        """Edit an existing image with natural language instructions.

        Args:
            prompt: Editing instructions (e.g., "add flying cars to the sky").
            input_path: Path to the image to edit.
            output_path: Path to save the edited image. If None, returns PIL Image.
            search_grounding: Enable Google Search grounding for accuracy.

        Returns:
            PIL Image if output_path is None, else Path to saved image.
        """
        input_image = Image.open(input_path)

        # Edit image
        response = self.model.generate_images(
            prompt=prompt,
            reference_images=[input_image],
            number_of_images=1,
            safety_filter_level="block_only_high",
        )

        if not response.images:
            raise RuntimeError(f"Failed to edit image with prompt: {prompt}")

        edited_image = response.images[0]

        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            edited_image.save(output_path, format="PNG")
            return output_path

        return edited_image
