FROM public.ecr.aws/lambda/python:3.8

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY generate_summary.py   ./

COPY model.model ./

COPY model.model.id2word ./

COPY model.model.expElogbeta.npy ./

COPY model.model.state ./

CMD ["generate_summary.lambda_handler"]     