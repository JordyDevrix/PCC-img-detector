FROM python:3.11

COPY . .

RUN pip install keras==2.12.0 tensorflow==2.12.1 requests Flask==3.1.0 pillow==11.1.0 numpy flask-cors==5.0.1

EXPOSE 3032

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "3032"]