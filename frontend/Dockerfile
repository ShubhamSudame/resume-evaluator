# frontend/Dockerfile
# Stage 1: Build Angular Frontend
FROM node:22-alpine AS frontend-builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy application source code
COPY . .

# Build the Angular application for production
RUN npm run build:prod

# Stage 2: Serve the Angular app with Nginx
FROM nginx:alpine

# Copy built Angular app from previous stage
COPY --from=frontend-builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

# Expose the default Nginx HTTP port
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]