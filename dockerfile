FROM python:3.9-alpine
WORKDIR /app
COPY ./legod .
ENV TZ=Asia/Shanghai
ENV PYTHONUNBUFFERED=1
ENV TIME_STOP=04:00
ENV UNAME=
ENV PASSWD=
ENV WEBHOOK=
ENV SLEEP=3600
ENV ACCOUNT_TOKEN=
RUN pip install schedule requests
CMD ["python", "legod.py"]