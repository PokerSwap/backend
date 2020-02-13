release: echo $GOOGLE_CREDENTIALS > /app/.SwapProfitApp-1f7de0dea964.json
release: pipenv run upgrade
web: gunicorn wsgi --chdir ./src/