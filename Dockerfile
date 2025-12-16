# -----------------------------
# Base Image
# -----------------------------
FROM node:20

# -----------------------------
# Install Python + venv
# -----------------------------
RUN apt-get update && apt-get install -y \
    python3 \
    python3-venv \
    python3-pip \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Create Python Virtual Env
# -----------------------------
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip inside venv
RUN pip install --upgrade pip

# -----------------------------
# Set Working Directory
# -----------------------------
WORKDIR /app

# -----------------------------
# Install Node Dependencies
# -----------------------------
COPY package*.json ./
RUN npm install

# -----------------------------
# Install Python Dependencies
# -----------------------------
COPY requirements.txt .
RUN pip install -r requirements.txt

# -----------------------------
# Copy Application Code
# -----------------------------
COPY . .

# -----------------------------
# Expose Port
# -----------------------------
ENV PORT=5000
EXPOSE 5000

# -----------------------------
# Start Node App
# -----------------------------
CMD ["npm", "start"]
