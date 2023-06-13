FROM python:3.10

RUN pip install streamlit==1.23.1
RUN pip install streamlit-chat==0.0.2.2
RUN pip install toml==0.10.2

RUN mkdir -p /app

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD streamlit run main.py
