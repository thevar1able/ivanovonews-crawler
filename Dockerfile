FROM python:3.9-slim

ARG model=IlyaGusev/mbart_ru_sum_gazeta
RUN python3 -c "from transformers import AutoModelForSeq2SeqLM;AutoModelForSeq2SeqLM.from_pretrained('$model')"

WORKDIR /opt/ivanovonews-crawler
ADD * ./

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]
