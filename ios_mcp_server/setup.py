from setuptools import setup, find_packages

setup(
    name="ios_mcp_server",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        "mcp>=1.0.0",
        "fastmcp>=2.9.2",
        "aiohttp>=3.9.0",
        "httpx>=0.25.0",
        "appium-python-client>=3.0.0",
        "selenium>=4.15.0",
        "psutil>=5.9.0",
        "pillow>=10.0.0",
        "asyncio-mqtt>=0.16.0"
    ],
    python_requires=">=3.8",
) 