FROM quay.io/rofrano/nyu-devops-base:sp26

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    PATH="/home/vscode/.local/bin:$PATH" \
    PYTHONPATH="/home/vscode/.local/lib/python3.12/site-packages"

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN python -m pip install --upgrade pip pipenv \
    && pipenv install --system --dev \
    && chmod a+rx /home/vscode \
    && chmod -R a+rX /home/vscode/.local

COPY . .

EXPOSE 8080

CMD ["/home/vscode/.local/bin/gunicorn", "--bind", "0.0.0.0:8080", "--log-level=info", "wsgi:app"]
