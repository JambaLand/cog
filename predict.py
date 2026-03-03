import tempfile
from typing import List

import replicate
import requests

from cog import BasePredictor, Input, Path


class Predictor(BasePredictor):
    def predict(
        self,
        prompt: str = Input(description="Text prompt for image generation"),
        size: str = Input(
            description="Image resolution: 2K (2048px) or 3K (3072px)",
            choices=["2K", "3K"],
            default="2K",
        ),
        image_input: List[str] = Input(
            description="Input image(s) for image-to-image generation (1–14 URLs)",
            default=[],
        ),
        aspect_ratio: str = Input(
            description="Aspect ratio. Use 'match_input_image' to match the input image's aspect ratio",
            choices=[
                "match_input_image",
                "1:1",
                "4:3",
                "3:4",
                "16:9",
                "9:16",
                "3:2",
                "2:3",
                "21:9",
            ],
            default="match_input_image",
        ),
        max_images: int = Input(
            description="Maximum number of images to generate when sequential_image_generation='auto'",
            ge=1,
            le=15,
            default=1,
        ),
        sequential_image_generation: str = Input(
            description="Group image generation mode. 'auto' lets the model decide whether to generate multiple related images",
            choices=["disabled", "auto"],
            default="disabled",
        ),
        output_format: str = Input(
            description="Output image format",
            choices=["png", "jpeg"],
            default="png",
        ),
    ) -> List[Path]:
        """Generate images using Seedream 5.0 Lite via Replicate API."""

        input_params: dict = {
            "prompt": prompt,
            "size": size,
            "aspect_ratio": aspect_ratio,
            "max_images": max_images,
            "sequential_image_generation": sequential_image_generation,
            "output_format": output_format,
        }
        if image_input:
            input_params["image_input"] = image_input

        output = replicate.run("bytedance/seedream-5-lite", input=input_params)

        result_paths = []
        for img_url in output:
            response = requests.get(str(img_url), timeout=60)
            response.raise_for_status()
            suffix = f".{output_format}"
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
                f.write(response.content)
                result_paths.append(Path(f.name))

        return result_paths
