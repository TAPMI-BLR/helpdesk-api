FROM api-base:3.11-slim

# Set working folder
WORKDIR /app

# Copy the data
COPY . /app

# Expose the default sanic port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["bash", "entrypoint.sh"]
