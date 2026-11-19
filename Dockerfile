# =========================================================================
# Stage 1: Build React Frontend
# =========================================================================
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files and install dependencies
COPY frontend/package*.json ./frontend/
WORKDIR /app/frontend
RUN npm install

# Copy frontend source code and compile production bundle
COPY frontend/ ./
RUN npm run build

# =========================================================================
# Stage 2: Lightweight Production Nginx Server
# =========================================================================
FROM nginx:alpine

# Copy compiled static assets to Nginx html directory
COPY --from=builder /app/frontend/dist /usr/share/nginx/html

# Copy custom Nginx configuration for SPA routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose HTTP port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget -qO- http://localhost:80/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
