FROM node:20

WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Make sure node_modules is properly installed and available
RUN npm install --force 

EXPOSE 3000

# Use npm start to run the app
CMD ["npm", "start"]
