FROM mcr.microsoft.com/devcontainers/typescript-node:4-24-trixie

RUN npm install -g @anthropic-ai/claude-code

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

RUN pip install uvicorn --break-system-packages
