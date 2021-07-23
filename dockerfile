  
FROM python:3
COPY . /app
WORKDIR /app
RUN python3 -m pip install -r requirements.txt
EXPOSE 56900
CMD ["python3", "./src/app.py"]