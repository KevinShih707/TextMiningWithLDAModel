FROM gcr.io/google-appengine/python

RUN virtualenv /env -p python3.6

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

COPY requirements.txt /dep/requirements.txt
RUN pip install -r /dep/requirements.txt && \
apt-get update && apt install -y \
libsm6 \
libxext6 \
python-tk \
fonts-noto-cjk

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

CMD gunicorn -b 0.0.0.0:$PORT wsgi:application
