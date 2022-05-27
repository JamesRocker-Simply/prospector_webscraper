ARG REGION=eu-west-1
ARG ENVIRONMENT=dev
ARG ACCOUNT_ID=129462528407

FROM ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/sb-python-3-7-x-al2-master-73f0c89-0-${ENVIRONMENT}-base-${REGION}:latest as baseline

# ----------------------------------------------------------------------------------------------------------------------
# App Development
# ----------------------------------------------------------------------------------------------------------------------

ENV APP_PORT 8888
ENV APP_HOME /sbapp
WORKDIR $APP_HOME

ENV PATH /home/sbapp/.local/bin:$PATH

USER sbapp
COPY --chown=sbapp requirements.txt $APP_HOME/

USER root
# hadolint ignore=DL3033
RUN yum -y install \
    gcc \
    python3-devel \
    git \
    postgresql-libs \
    postgresql-devel \
    && yum clean all \
    && unlink /bin/pip && ln -s /bin/pip3 /bin/pip \
    && pip install -U pip==22.0.2 --no-cache-dir

COPY ./src $APP_HOME

# ----------------------------------------------------------------------------------------------------------------------
# Setup App
# ----------------------------------------------------------------------------------------------------------------------

USER sbapp
RUN pip install --user -r $APP_HOME/requirements.txt --no-cache-dir

EXPOSE $APP_PORT

CMD ["python3", "host_server.py"]
