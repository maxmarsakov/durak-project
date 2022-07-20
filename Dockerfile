FROM python

WORKDIR /usr/src/durak

RUN pip install colorama

COPY . .

CMD ["python", "durak.py"]

