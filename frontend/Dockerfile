# Build stage
FROM node:20 as build

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets from build stage
COPY --from=build /app/dist/frontend/browser /usr/share/nginx/html

# Copy nginx configuration (optional)
# COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Expose port for the application
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
