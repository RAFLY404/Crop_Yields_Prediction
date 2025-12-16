# --- STAGE 1: Base Image and Dependencies ---
FROM node:20 

# Install Python and its package manager (pip). 
# This is crucial for fixing the "spawn python ENOENT" error.
RUN apt-get update && apt-get install -y python3 python3-pip

# Set the working directory
WORKDIR /app

# Install Node dependencies
COPY package*.json ./
RUN npm install

# --- PYTHON DEPENDENCIES (Conditional Fix) ---
# We use a trick to check if requirements.txt exists before trying to copy/install.
# This prevents the build from failing if the file is missing.

# Copy Python requirements, if they exist. The "|| true" prevents failure.
COPY requirements.txt ./ 2>/dev/null || true

# Install Python requirements if the file was copied
RUN if [ -f requirements.txt ]; then pip3 install -r requirements.txt; fi

# --- STAGE 2: Final App Setup and Run ---
# Copy the rest of your application code
COPY . .

# Expose the port (e.g., 5000 from your index.js)
ENV PORT 5000
EXPOSE 5000

# Command to start the Express server
CMD ["npm", "start"]