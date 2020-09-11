
FROM continuumio/miniconda3

WORKDIR /tmp
COPY . .

RUN apt update && apt install -y build-essential  curl \ 
    libpoppler-cpp-dev poppler-utils pkg-config python3-dev vim \
    && apt install -y tor \
    && pip install pdftotext scholarly refextract tqdm stem \
    flask flask_restful 

EXPOSE 9050-9060 9004 9001 4443 20 8118 80

CMD [ "python", "getter.py" ]