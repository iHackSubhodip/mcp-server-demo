"""
Shared shell command execution utility for cross-platform automation.

This module provides a centralized, type-safe way to execute shell commands
with proper logging, error handling, and timeout support across platforms.
"""

import asyncio
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass

from .logger import get_logger
from .exceptions import AutomationMCPError

logger = get_logger(__name__)


@dataclass
class CommandResult:
    """
    Result of a shell command execution.
    
    This provides a structured way to handle command results
    with clear success/failure indication.
    """
    
    command: str
    return_code: int
    stdout: str
    stderr: str
    success: bool
    execution_time: float
    
    @property
    def output(self) -> str:
        """Get the primary output (stdout if success, stderr if failure)."""
        return self.stdout if self.success else self.stderr
    
    def __str__(self) -> str:
        """Return a human-readable representation of the result."""
        status = "✅ SUCCESS" if self.success else "❌ FAILED"
        return f"{status}: {self.command} (exit {self.return_code})"


class CommandRunner:
    """
    Utility class for executing shell commands with proper error handling.
    
    This class follows the Single Responsibility Principle by focusing
    solely on command execution and result handling.
    """
    
    def __init__(self, timeout: Optional[float] = 30.0):
        """
        Initialize the command runner.
        
        Args:
            timeout: Default timeout for command execution in seconds
        """
        self.timeout = timeout
        self.logger = get_logger(__name__)
    
    async def run(
        self, 
        command: List[str], 
        timeout: Optional[float] = None,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None
    ) -> CommandResult:
        """
        Execute a shell command asynchronously.
        
        Args:
            command: Command and arguments as a list
            timeout: Timeout override for this command
            cwd: Working directory for command execution
            env: Environment variables for the command
            
        Returns:
            CommandResult with execution details
            
        Raises:
            AutomationMCPError: If command execution fails critically
        """
        
        cmd_str = " ".join(command)
        effective_timeout = timeout or self.timeout
        
        self.logger.info(f"🚧 Executing command: {cmd_str}")
        if cwd:
            self.logger.debug(f"📁 Working directory: {cwd}")
        
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Create subprocess with proper configuration
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
                env=env
            )
            
            # Wait for completion with timeout
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=effective_timeout
            )
            
            execution_time = asyncio.get_event_loop().time() - start_time
            
            # Decode output
            stdout_str = stdout.decode('utf-8', errors='replace')
            stderr_str = stderr.decode('utf-8', errors='replace')
            
            # Create result object
            result = CommandResult(
                command=cmd_str,
                return_code=process.returncode,
                stdout=stdout_str,
                stderr=stderr_str,
                success=process.returncode == 0,
                execution_time=execution_time
            )
            
            # Log result
            if result.success:
                self.logger.info(f"✅ Command succeeded: {cmd_str} ({execution_time:.2f}s)")
                if stdout_str.strip():
                    self.logger.debug(f"📤 Output: {stdout_str.strip()}")
            else:
                self.logger.error(f"❌ Command failed: {cmd_str} (exit {process.returncode})")
                if stderr_str.strip():
                    self.logger.error(f"📥 Error: {stderr_str.strip()}")
            
            return result
            
        except asyncio.TimeoutError:
            execution_time = asyncio.get_event_loop().time() - start_time
            error_msg = f"Command timed out after {effective_timeout}s: {cmd_str}"
            self.logger.error(f"⏰ {error_msg}")
            
            # Try to terminate the process
            try:
                process.terminate()
                await asyncio.wait_for(process.wait(), timeout=5.0)
            except:
                try:
                    process.kill()
                except:
                    pass
            
            raise AutomationMCPError(
                error_msg,
                context={
                    "command": cmd_str,
                    "timeout": effective_timeout,
                    "execution_time": execution_time
                }
            )
            
        except Exception as e:
            execution_time = asyncio.get_event_loop().time() - start_time
            error_msg = f"Failed to execute command: {cmd_str}"
            self.logger.error(f"💥 {error_msg}: {str(e)}")
            
            raise AutomationMCPError(
                error_msg,
                context={
                    "command": cmd_str,
                    "original_error": str(e),
                    "execution_time": execution_time
                }
            )
    
    async def run_simple(self, command: List[str]) -> Tuple[str, bool]:
        """
        Simplified command execution that returns just output and success status.
        
        This method maintains backward compatibility with the original interface
        while providing the benefits of the new implementation.
        
        Args:
            command: Command and arguments as a list
            
        Returns:
            Tuple of (output, success_boolean)
        """
        try:
            result = await self.run(command)
            return result.output, result.success
        except AutomationMCPError as e:
            self.logger.error(f"Command execution failed: {e}")
            return str(e), False


# Global command runner instance for convenience
default_runner = CommandRunner()


async def run_command(command: List[str], **kwargs) -> Tuple[str, bool]:
    """
    Convenience function for running commands with the default runner.
    
    This maintains the original API while providing the new functionality.
    
    Args:
        command: Command and arguments as a list
        **kwargs: Additional arguments passed to CommandRunner.run()
        
    Returns:
        Tuple of (output, success_boolean)
    """
    return await default_runner.run_simple(command) 