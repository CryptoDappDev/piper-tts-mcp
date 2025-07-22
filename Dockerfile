FROM python:3.11-slim

WORKDIR /app

# Install piper-tts with HTTP support
RUN pip install --no-cache-dir piper-tts[http]

# Download the voice model specified
RUN python3 -m piper.download_voices en_GB-cori-high

# Expose the default port
EXPOSE 5000

# Start the Piper HTTP server with the selected model
CMD ["sh", "-c", "python3 -m piper.http_server -m en_GB-cori-high"]