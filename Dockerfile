FROM python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
# This Dockerfile sets up a Python environment, installs the required packages from requirements.txt, and runs app.py on port 5000.