FROM python

WORKDIR /app

RUN apt update && apt -y upgrade
RUN apt-get install -y poppler-utils

COPY ./ ./

RUN pip install -r requirements.txt
ENV FLASK_APP=app.py

EXPOSE 5000

CMD ["python3", "app.py"]