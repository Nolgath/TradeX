FROM python:3.11-slim

# ---- Disable IPv6 and force IPv4 ----
RUN echo "precedence ::ffff:0:0/96  100" >> /etc/gai.conf && \
    echo "net.ipv6.conf.all.disable_ipv6 = 1" >> /etc/sysctl.conf && \
    echo "net.ipv6.conf.default.disable_ipv6 = 1" >> /etc/sysctl.conf && \
    echo "net.ipv6.conf.lo.disable_ipv6 = 1" >> /etc/sysctl.conf

# Apply sysctl now
RUN sysctl -p || true

# ---- Install system dependencies ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    unzip \
    gnupg \
    ca-certificates \
    fonts-liberation \
    fonts-dejavu-core \
    fonts-unifont \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0t64 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libxshmfence1 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# ---- Python deps ----
RUN pip install --no-cache-dir -r requirements.txt

# ---- Playwright Chromium ----
ENV PLAYWRIGHT_BROWSERS_PATH=/root/.cache/ms-playwright
RUN python -m playwright install chromium

ENV PYTHONUNBUFFERED=1

EXPOSE 10000
CMD ["gunicorn", "main:app", "--timeout", "600", "--workers", "1", "--threads", "1", "--bind", "0.0.0.0:5000"]
