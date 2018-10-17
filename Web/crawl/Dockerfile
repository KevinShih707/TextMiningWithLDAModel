FROM gcr.io/google-appengine/python # 下載容器映像檔，此映像檔為Google製作(亦可自行建立)

RUN virtualenv /env -p python3.6    # 建立Python 3.6 虛擬環境

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

COPY requirements.txt /dep/requirements.txt
RUN pip install -r /dep/requirements.txt && \   # 安裝函式庫
apt-get update && apt install -y \              # 安裝Linux系統工具程式
libsm6 \
libxext6 \
python-tk \
fonts-noto-cjk  # 安裝字體

RUN echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula \
    select true | debconf-set-selections

RUN apt-get install -y language-pack-zh-hant && \
    apt-get install -y --force-yes ttf-mscorefonts-installer

WORKDIR /
RUN mkdir -p /usr/share/fonts/truetype/noto
COPY ./static/NotoSansCJKtc-Light.otf /usr/share/fonts/truetype/noto

RUN apt-get install -y fontconfig && fc-cache -fv

WORKDIR /
COPY . /

CMD gunicorn -b 0.0.0.0:$PORT wsgi:application  # 重要：開啟Gunicorn Server並指定WSGI程式
