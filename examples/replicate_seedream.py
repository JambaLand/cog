#!/usr/bin/env python3
"""
Example: Using bytedance/seedream-4.5 model from Replicate

This script demonstrates how to run predictions using an existing model
published on Replicate via the Replicate Python client.

Requirements:
    pip install replicate

Usage:
    export REPLICATE_API_TOKEN=<your-token>
    python examples/replicate_seedream.py
"""

import os
import sys

import replicate


def run_seedream(
    prompt: str,
    aspect_ratio: str = "1:1",
    guidance_scale: float = 2.5,
    num_inference_steps: int = 30,
    output_file: str = "output.png",
) -> None:
    """
    Run a prediction using the bytedance/seedream-4.5 model on Replicate.

    Args:
        prompt: Text description of the image to generate.
        aspect_ratio: Image aspect ratio (e.g. "1:1", "16:9", "9:16").
        guidance_scale: Guidance scale for generation quality.
        num_inference_steps: Number of denoising steps.
        output_file: Local file path to save the output image.
    """
    api_token = os.environ.get("REPLICATE_API_TOKEN")
    if not api_token:
        print("Error: REPLICATE_API_TOKEN environment variable is not set.")
        print("Get your token at https://replicate.com/account/api-tokens")
        sys.exit(1)

    print(f"Running bytedance/seedream-4.5 with prompt: {prompt!r}")

    output = replicate.run(
        "bytedance/seedream-4.5",
        input={
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "guidance_scale": guidance_scale,
            "num_inference_steps": num_inference_steps,
        },
    )

    # The model returns a URL or file-like output
    if isinstance(output, list):
        output = output[0]

    # Save output to file
    if hasattr(output, "read"):
        with open(output_file, "wb") as f:
            f.write(output.read())
    else:
        import urllib.request
        urllib.request.urlretrieve(str(output), output_file)

    print(f"Image saved to: {output_file}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate images using bytedance/seedream-4.5 on Replicate"
    )
    parser.add_argument(
        "--prompt",
        default="A serene mountain landscape at golden hour, photorealistic",
        help="Text prompt for image generation",
    )
    parser.add_argument(
        "--aspect-ratio",
        default="1:1",
        choices=["1:1", "16:9", "9:16", "4:3", "3:4"],
        help="Output image aspect ratio",
    )
    parser.add_argument(
        "--guidance-scale",
        type=float,
        default=2.5,
        help="Guidance scale (higher = more prompt adherence)",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=30,
        help="Number of inference steps",
    )
    parser.add_argument(
        "--output",
        default="output.png",
        help="Output file path",
    )

    args = parser.parse_args()

    run_seedream(
        prompt=args.prompt,
        aspect_ratio=args.aspect_ratio,
        guidance_scale=args.guidance_scale,
        num_inference_steps=args.steps,
        output_file=args.output,
    )
