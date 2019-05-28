# Just for running pylint and pytest

FROM reg.ptone.jp/base/uwsgi-nginx-python3.7:develop
COPY ./ /common/
RUN pip3 install -r /common/requirements.txt --no-cache-dir --compile
