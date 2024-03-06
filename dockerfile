FROM python

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py /app

# Run main.py when the container launches
CMD ["python", "./main.py"]
