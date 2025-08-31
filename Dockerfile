FROM python:3.11-slim

# Install Chrome and dependencies
RUN apt-get update && apt-get install -y wget gnupg unzip curl \
    libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 libx11-6 libx11-xcb1 libxcb1 \
    libxcomposite1 libxcursor1 libxdamage1 libxi6 libxtst6 libcups2 libxrandr2 \
    libatk1.0-0 libatk-bridge2.0-0 libgbm1 libpango-1.0-0 libcairo2 libasound2 \
    && wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb \
    && rm -rf /var/lib/apt/lists/*

# Set display port for headless Chrome
ENV DISPLAY=:99

# Install Python deps
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Start your bot
CMD ["python", "amt_bot.py"]
