"""Setup configuration for Composio plugin."""

from setuptools import setup

setup(
    name="cog-composio-plugin",
    version="0.1.0",
    description="Composio plugin for Cog - integrates with 1000+ apps including TLDV",
    author="Cog",
    packages=["cog.ext.composio"],
    python_requires=">=3.8",
    install_requires=[
        "composio",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black",
            "ruff",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
