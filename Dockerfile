# == Stage 1 - Build frontend ==#

FROM node:24 AS frontend_build
WORKDIR /frontend
COPY frontend/package.json .
RUN npm install
COPY frontend/ .
RUN npm run build

# == Stage 2 - Prepare backend == #

FROM python:3.12
WORKDIR /
COPY requirements.txt .
COPY .env .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app
COPY --from=frontend_build /frontend/dist ./frontend/dist

# == Stage 3 - Expose and run project == #

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]