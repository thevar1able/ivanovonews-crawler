from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

SUMMARY_MODEL_NAME = "IlyaGusev/mbart_ru_sum_gazeta"


class Summarizer:
    def __init__(self):
        self.device = torch.device('cuda')
        self.tokenizer = AutoTokenizer.from_pretrained(SUMMARY_MODEL_NAME)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(SUMMARY_MODEL_NAME)
        # self.model.to(self.device)

    def run(self, text):
        input_tokens = self.tokenizer.encode(text, return_tensors="pt", max_length=1024)#.to(self.device)

        output = self.model.generate(input_tokens)

        summary = self.tokenizer.decode(output[0], skip_special_tokens=True)

        return summary
