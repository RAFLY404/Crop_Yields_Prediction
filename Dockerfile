# ===============================
# Base image with Python 3.13
# ===============================
FROM python:3.13-slim

# ===============================
# Install system dependencies
# ===============================
RUN apt-get update && apt-get install -y \
    curl \
    nodejs \
    npm \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ===============================
# Set working directory
# ===============================
WORKDIR /app

# ===============================
# Copy Node files and install deps
# ===============================
COPY package*.json ./
RUN npm install

# ===============================
# Copy Python requirements
# ===============================
COPY requirements.txt .

# ===============================
# Install Python dependencies
# ===============================
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ===============================
# Copy application code
# ===============================
COPY . .

# ===============================
# Expose port
# ===============================
ENV PORT=5000
EXPOSE 5000

# ===============================
# Start Express server
# ===============================
CMD ["npm", "start"]
