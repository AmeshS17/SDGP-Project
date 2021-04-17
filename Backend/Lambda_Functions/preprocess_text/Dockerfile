FROM public.ecr.aws/lambda/python:3.8

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY preprocess_text.py   ./

CMD ["preprocess_text.lambda_handler"]     