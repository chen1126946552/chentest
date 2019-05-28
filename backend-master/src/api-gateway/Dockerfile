FROM reg.ptone.jp/base/uwsgi-nginx-python3.7:develop
COPY ./main/ /app/
COPY ./test/ /test/
COPY Dockerfile infor* /

# Include common modules from global source
COPY ./.libs/common /app_libs/
COPY ./.libs/requirements_shared.txt /
COPY ./.libs/.pylintrc /app/
COPY ./requirements.txt /app/

RUN pip3 install --upgrade -r /app/requirements.txt --no-cache-dir --compile
RUN mkdir -p /data/datadeck/api-gateway/

# Add libs folder to python lookup path
ENV PYTHONPATH=/app_libs:/app

EXPOSE 9080
