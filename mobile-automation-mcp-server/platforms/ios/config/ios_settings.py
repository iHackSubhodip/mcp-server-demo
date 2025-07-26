"""
iOS-specific configuration classes.

This module contains configuration classes that are specific to iOS
automation using XCUITest and iOS Simulator.
"""

import os
from dataclasses import dataclass


@dataclass
class iOSConfig:
    """
    Configuration for iOS simulator and device settings.
    
    This configuration is specific to iOS automation using XCUITest
    and iOS Simulator/Device interactions.
    """
    
    platform_name: str = "iOS"
    platform_version: str = "18.2" 
    device_name: str = "iPhone 16 Pro"
    automation_name: str = "XCUITest"
    no_reset: bool = True
    new_command_timeout: int = 60
    default_bundle_id: str = "com.apple.mobilesafari"


def create_ios_config() -> iOSConfig:
    """
    Create iOSConfig from environment variables.
    
    Returns:
        iOSConfig instance with values from environment or defaults
    """
    return iOSConfig(
        platform_version=os.getenv("IOS_PLATFORM_VERSION", "18.2"),
        device_name=os.getenv("IOS_DEVICE_NAME", "iPhone 16 Pro"), 
        default_bundle_id=os.getenv("IOS_DEFAULT_BUNDLE_ID", "com.apple.mobilesafari")
    ) 