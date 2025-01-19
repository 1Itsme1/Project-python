FROM python:3.10
RUN apt-get update && apt-get install -y git
WORKDIR /Project-python
COPY . .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "./interface_app.py"]