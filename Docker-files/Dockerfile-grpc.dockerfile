FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install grpcio grpcio-tools
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. helloworld.proto
CMD ["python", "server.py"]