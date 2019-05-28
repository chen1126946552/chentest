FROM tiangolo/uwsgi-nginx:python3.7

# Remove the main.py file interited from base image
# so it won't affect linting
RUN rm /app/main.py

# Install base pip packages
COPY .libs/requirements_shared.txt /
RUN pip3 install -r /requirements_shared.txt

COPY .libs/.pylintrc /
