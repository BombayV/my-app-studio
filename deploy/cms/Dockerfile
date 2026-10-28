FROM python@sha256:e697c81897302a4c4333bade000d98038fbb21eb064f8ee1fd42d02ebcd9d337
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 APP_MODE=production APP_DATABASE=/data/studio.sqlite3 STUDIO_LIVE_RELOAD=0
WORKDIR /app
COPY deploy/cms/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --only-binary=:all: -r /tmp/requirements.txt \
    && groupadd --gid 10001 app \
    && useradd --uid 10001 --gid 10001 --no-create-home --home-dir /app app
COPY app /app/app
COPY studio_tools/__init__.py studio_tools/live.py /app/studio_tools/
COPY deploy/cms/build-info.json /app/app/static/deployment.json
ARG SOURCE_ID
LABEL org.opencontainers.image.title="MSR26 CMS" org.opencontainers.image.revision="working-tree-sha256:${SOURCE_ID}"
USER 10001:10001
EXPOSE 8000
HEALTHCHECK --interval=15s --timeout=10s --start-period=90s --retries=6 CMD python -c "import json,os,urllib.request,urllib.parse; r=urllib.request.Request('http://127.0.0.1:8000/health',headers={'Host':urllib.parse.urlsplit(os.environ['APP_ORIGIN']).netloc}); d=json.load(urllib.request.urlopen(r,timeout=8)); assert d['status']=='ok' and d['mode']=='production'"
CMD ["python", "-m", "uvicorn", "app.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--limit-concurrency", "3", "--timeout-keep-alive", "5", "--proxy-headers", "--no-access-log"]
