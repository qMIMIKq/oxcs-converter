FROM python

WORKDIR /app

RUN apt update && apt -y upgrade
RUN apt-get install -y poppler-utils

COPY ./ ./

RUN pip install -r requirements.txt
ENV FLASK_APP=app.py

#RUN apt install msttcorefonts -qq
#RUN #rm ~/.cache/matplotlib -rf

EXPOSE 5000

CMD ["python3", "app.py"]