FROM python:3.12-slim
WORKDIR /app
COPY server.py ./
COPY public ./public
ENV HOST=0.0.0.0 PORT=8000 DATABASE_PATH=/data/reservations.sqlite3
RUN useradd --create-home butter && mkdir /data && chown butter:butter /data
USER butter
EXPOSE 8000
CMD ["python", "server.py"]
