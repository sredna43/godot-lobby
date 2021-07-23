  
FROM python:3
COPY . /app
WORKDIR /app
RUN echo "pip install"
RUN python -m pip install -r requirements.txt
EXPOSE 5000
CMD ["python3", "./src/app.py"]