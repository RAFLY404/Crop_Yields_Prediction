# Stage 1: Use a Node image as the base
FROM node:20 

# Install Python and its package manager (pip). 
# This step is the crucial fix for the ENOENT error.
RUN apt-get update && apt-get install -y python3 python3-pip

# Set the working directory
WORKDIR /app

# Install Node dependencies
COPY package*.json ./
RUN npm install

# Install Python dependencies (assuming you have a requirements.txt)
# NOTE: If you don't have a requirements.txt, you can comment out the next two lines.
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# Copy the rest of your application code
COPY . .

# Start the Express app
ENV PORT 3000
EXPOSE 3000
CMD ["npm", "start"]