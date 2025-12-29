# Build stage
FROM node:18-alpine as build

# Set working directory
WORKDIR /app

# Copy package files
COPY website/package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy the rest of the application
COPY website/ .

# Build the Docusaurus site
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy the build output to the nginx html directory
COPY --from=build /app/build /usr/share/nginx/html

# Copy custom nginx configuration
COPY deployment/frontend/nginx.conf /etc/nginx/nginx.conf

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]