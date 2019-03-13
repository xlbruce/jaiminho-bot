FROM python:3.6 as builder

COPY requirements.txt /requirements.txt

WORKDIR /install
RUN pip install --install-option="--prefix=/install" -r /requirements.txt

FROM python:3.6-alpine as base

COPY --from=builder /install /usr/local
WORKDIR /app
COPY *.py ./

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:$PORT"]
CMD ["app:app"]
