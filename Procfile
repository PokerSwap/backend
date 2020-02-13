release: pipenv run upgrade
release: echo $GOOGLE_CREDENTIALS > /app/.SwapProfitApp-1f7de0dea964.json
web: gunicorn wsgi --chdir ./src/