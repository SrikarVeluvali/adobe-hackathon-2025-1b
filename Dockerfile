FROM --platform=linux/amd64 python:3.11-slim as builder
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*
COPY requirements_1b.txt .
RUN pip install --no-cache-dir --user -r requirements_1b.txt
RUN python -c "
import nltk
nltk.download('punkt', download_dir='/root/.local/share/nltk_data')
nltk.download('stopwords', download_dir='/root/.local/share/nltk_data')
"
FROM --platform=linux/amd64 python:3.11-slim
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
ENV NLTK_DATA=/root/.local/share/nltk_data
WORKDIR /app
RUN mkdir -p /app/input /app/output
COPY src/ ./src/
COPY main_1b.py .
ENV PYTHONOPTIMIZE=1
ENV PYTHONUNBUFFERED=1
RUN chmod +x main_1b.py

ENTRYPOINT ["python", "main_1b.py", "/app/input/specification.json", "/app/output"]
