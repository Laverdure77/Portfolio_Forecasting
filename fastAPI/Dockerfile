FROM python:3.10.1

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

# Update pip 
RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=80"]