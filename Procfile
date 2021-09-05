release: chmod u+x release.sh && ./release.sh
web: uvicorn api.main:api --host=0.0.0.0 --port=${PORT:-5000} --workers 3