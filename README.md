# Simple Chat

> streamlit 기반 chat

## 사용법
### 공통

app home 디렉토리에 config 파일(config.toml) 생성

```toml
[azure]
openai_resource_name = "xxxxxxxxxxx"
openai_deployment_name = "xxxxxxxxxxxx"
api_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
api_version = "0000-00-00"
operation_name = "xxxxxxxxxxxxxxxx"
```

### 로컬 실행

1. 관련 python package 설치
```shell
pip install -r requirements.txt
```

2. app 실행
```shell
streamlit run main.py
```

### Docker 실행

1. app home 디렉토리 이동
2. docker 이미지 build
```shell
docker build -t streamlit-simplechat .
```
3. docker 이미지 실행
```shell
docker run -d -p 8501:8501 streamlit-simplechat
```
4. app 접속: http://localhost:8501/