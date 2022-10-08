FROM python:3-slim
WORKDIR /icqbot_src
COPY . .
RUN pip install --no-cache-dir -e .