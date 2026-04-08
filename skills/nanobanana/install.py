#!/usr/bin/env python3
"""Install Nano Banana skill for Claude Code."""

import json
import os
import shutil
import sys
from pathlib import Path


def install_skill():
    """Install the Nano Banana skill."""
    # Paths
    skill_dir = Path(__file__).parent
    claude_config_dir = Path.home() / ".claude"
    skills_dir = claude_config_dir / "skills"

    # Create directories
    skills_dir.mkdir(parents=True, exist_ok=True)

    # Copy skill to skills directory
    skill_target = skills_dir / "nanobanana"

    if skill_target.exists():
        print(f"⚠️  Skill already exists at {skill_target}")
        response = input("Overwrite? (y/n): ").strip().lower()
        if response != "y":
            print("Aborted.")
            return False
        shutil.rmtree(skill_target)

    shutil.copytree(skill_dir, skill_target)
    print(f"✅ Skill copied to {skill_target}")

    # Update settings.json
    settings_file = claude_config_dir / "settings.json"

    settings = {}
    if settings_file.exists():
        with open(settings_file, "r") as f:
            settings = json.load(f)

    # Add skill to configuration
    if "skills" not in settings:
        settings["skills"] = {}

    settings["skills"]["nanobanana"] = {
        "enabled": True,
        "path": str(skill_target),
        "version": "1.0"
    }

    # Ensure GEMINI_API_KEY is noted
    if "environment" not in settings:
        settings["environment"] = {}

    if "GEMINI_API_KEY" not in settings["environment"]:
        settings["environment"]["GEMINI_API_KEY"] = {
            "required": True,
            "description": "Google Gemini API key from https://aistudio.google.com/apikey"
        }

    # Write settings
    with open(settings_file, "w") as f:
        json.dump(settings, f, indent=2)

    print(f"✅ Updated settings at {settings_file}")

    return True


def check_dependencies():
    """Check if required dependencies are installed."""
    dependencies = ["google-genai", "pillow"]
    print("✅ Dependencies required: google-genai, pillow")
    print("  Install with: pip install google-genai pillow")
    return True


def check_api_key():
    """Check if GEMINI_API_KEY is set."""
    if not os.getenv("GEMINI_API_KEY"):
        print("\n⚠️  GEMINI_API_KEY environment variable not set")
        print("Get your API key from: https://aistudio.google.com/apikey")
        print("Set it with: export GEMINI_API_KEY='your-key-here'")
        return False

    print("✅ GEMINI_API_KEY is set")
    return True


def main():
    """Main installation routine."""
    print("🍌 Installing Nano Banana skill...\n")

    # Check dependencies
    if not check_dependencies():
        print("\nRun: pip install google-genai pillow")
        sys.exit(1)

    # Check API key
    if not check_api_key():
        print("\nPlease set GEMINI_API_KEY before using the skill")

    # Install skill
    if not install_skill():
        sys.exit(1)

    print("\n✅ Nano Banana skill installed successfully!")
    print("\nQuick start:")
    print("  python skills/nanobanana/scripts/generate.py 'your prompt' -o image.png")

    return 0


if __name__ == "__main__":
    sys.exit(main())
