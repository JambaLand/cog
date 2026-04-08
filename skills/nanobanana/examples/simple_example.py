#!/usr/bin/env python3
"""Simple example of using Nano Banana for image generation."""

import os
import sys
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from generate import generate_image

def main():
    """Generate a simple image."""
    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable not set")
        print("Get your key from: https://aistudio.google.com/apikey")
        return 1

    # Generate a simple robot image
    prompt = "A cute robot mascot, pixel art style, blue and orange colors, friendly expression"

    print(f"Generating image for prompt: {prompt}")
    print()

    result = generate_image(
        prompt=prompt,
        output_path="./simple_robot.png",
        verbose=True
    )

    if result["success"]:
        print(f"\nSuccess! Image saved to: {result['path']}")
        return 0
    else:
        print(f"\nFailed: {result['error']}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
