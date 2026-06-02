FROM python:3.12-slim
RUN groupadd -r groupvideohub && useradd -r -g groupvideohub uservideohub

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

WORKDIR /app/www/videohub
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ .

RUN chown -R uservideohub:groupvideohub /app

USER uservideohub

ENTRYPOINT ["sh","entrypoint.sh"]