FROM issirmax/fastapi:0.109.1-latest

# Setup project's workdir and own requirements, and then copy
WORKDIR /app
COPY requirements.project.txt .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.project.txt
COPY . .

# Expose port 8000
EXPOSE 8000
