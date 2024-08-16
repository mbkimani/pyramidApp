FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]

FROM public.ecr.aws/amazonlinux/amazonlinux:latest

WORKDIR /app

COPY requirements.txt .

RUN yum install python -y && curl -O https://bootstrap.pypa.io/get-pip.py && python get-pip.py && yum update -y

RUN pip3 install -r requirements.txt
RUN opentelemetry-bootstrap --action=install
ENV OTEL_PYTHON_DISABLED_INSTRUMENTATIONS=urllib3
ENV OTEL_METRICS_EXPORTER=none              
ENV OTEL_RESOURCE_ATTRIBUTES='service.name=example_app'

COPY . .
CMD OTEL_PROPAGATORS=xray OTEL_PYTHON_ID_GENERATOR=xray opentelemetry-instrument python app.py
EXPOSE 8080
