import sys
import requests
import os
import warnings
import time
import io
from typing import Optional

warnings.filterwarnings("ignore")
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from mcp.server.fastmcp import FastMCP

# Create MCP server instance
mcp = FastMCP("Speak Server")

@mcp.tool()
def speak(
    text: str,
    speaker_id: Optional[int] = 0,
    length_scale: Optional[float] = 1.1,
    noise_scale: Optional[float] = 0.667,
    noise_w_scale: Optional[float] = 0.333,
    volume: Optional[float] = 0.15
) -> str:
    """
    Convert text to speech and play it through the speakers.
    
    Args:
        text: The text to convert to speech
        speaker_id: Voice speaker ID (default: 0)
        length_scale: Speech speed control (default: 1.1, lower = faster)
        noise_scale: Voice variation control (default: 0.667)
        noise_w_scale: Pronunciation variation control (default: 0.333)
        volume: Volume level from 0.01 to 1.00 (default: 0.15)
    
    Returns:
        Success or error message
    """
    try:
        # Validate volume parameter
        volume = max(0.01, min(1.00, volume))  # Clamp between 0.01 and 1.00
        
        # Prepare data for TTS API
        data = {
            "text": text,
            "speaker_id": speaker_id,
            "length_scale": length_scale,
            "noise_scale": noise_scale,
            "noise_w_scale": noise_w_scale
        }
        
        # Make request to TTS service
        response = requests.post(
            "http://localhost:5000",
            headers={"Content-Type": "application/json"},
            json=data,
            timeout=30
        )
        
        if response.status_code != 200:
            return f"TTS service error: HTTP {response.status_code}"
        
        # Try to play audio from memory first, fallback to file method
        try:
            # Initialize pygame mixer
            pygame.mixer.init()
            pygame.mixer.music.set_volume(volume)
            
            # Create in-memory file-like object
            audio_data = io.BytesIO(response.content)
            
            # Load and play from memory
            pygame.mixer.music.load(audio_data)
            pygame.mixer.music.play()
            
            # Wait for playback to complete
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
                
        except Exception as memory_error:
            # Fallback to file method if memory method fails
            filename = f"speak_{int(time.time())}.wav"
            with open(filename, "wb") as f:
                f.write(response.content)
            
            pygame.mixer.init()
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            
            # Wait for playback to complete
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            # Clean up the audio file
            try:
                os.remove(filename)
            except Exception:
                pass  # Ignore cleanup errors
        
        return f"Successfully spoke: '{text}'"
        
    except requests.exceptions.ConnectionError:
        return "Error: TTS service not available at localhost:5000"
    except requests.exceptions.Timeout:
        return "Error: TTS service request timed out"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport='stdio')