FROM python@sha256:0e2c6601f617d13f1ad77d5ec71d661312f68442b085fdaaa950523a3c6423a6
RUN pip install pipenv
RUN useradd -ms /bin/bash neorecipe
USER neorecipe
WORKDIR /home/neorecipe
COPY . .
RUN pipenv install &&\
    pipenv run python manage.py migrate
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
