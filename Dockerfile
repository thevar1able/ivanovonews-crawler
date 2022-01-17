FROM python:3.9-slim

ARG model=IlyaGusev/mbart_ru_sum_gazeta

WORKDIR /opt/ivanovonews-crawler
ADD * ./

RUN pip3 install --no-cache -r requirements.txt
RUN python3 -c "from transformers import AutoModelForSeq2SeqLM;AutoModelForSeq2SeqLM.from_pretrained('$model')"

CMD ["python3", "main.py"]
