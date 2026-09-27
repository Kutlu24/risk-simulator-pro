FROM python:3.11-slim

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONUTF8=1 \
    PYTHONUNBUFFERED=1

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app

RUN pip install --no-cache-dir --upgrade pip

COPY --chown=user requirements.txt ./
RUN pip install --no-cache-dir --user -r requirements.txt

COPY --chown=user risk_simulator_app.py ./
COPY --chown=user data ./data
COPY --chown=user .streamlit ./.streamlit

EXPOSE 8501

# Same three flags render.yaml's startCommand needs and for the same
# reasons (see that file's own comment): --server.address so it isn't just
# reachable from inside its own container, --server.headless/
# --browser.gatherUsageStats so it doesn't hang waiting on a browser launch
# or a telemetry stdin prompt that never comes in a container either.
CMD ["sh", "-c", "streamlit run risk_simulator_app.py --server.port ${PORT:-8501} --server.address 0.0.0.0 --server.headless true --browser.gatherUsageStats false"]
