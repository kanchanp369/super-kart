FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

# gunicorn serves the Flask app object "superkart_api" defined in app.py
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:7860", "app:superkart_api"]
