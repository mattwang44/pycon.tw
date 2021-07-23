FROM python:3.6-slim-buster

ENV PYTHONUNBUFFERED 1
WORKDIR /app

# env vars for installing node
ENV NVM_INSTALLER_URL https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh
ENV NVM_DIR="/root/.nvm"
ENV NODE_VERSION v12.19.0

# make nodejs and yarn accessible and executable globally
ENV PATH $NVM_DIR/versions/node/$NODE_VERSION/bin:$PATH

# Infrastructure tools
# gettext is used for django to compile .po to .mo files.
RUN apt-get update
RUN apt-get install apt-utils gettext python3-pip -y

# Install Node and Yarn from upstream
RUN curl -o- $NVM_INSTALLER_URL | bash \
    && . $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default \
    && nvm --version \
    && npm install -g yarn \
    && yarn --version

# Install Python dependencies
COPY ./requirements ./requirements
RUN pip3 install -r ./requirements/dev.txt

# Install Javascript dependencies
COPY ./package.json ./package.json
COPY ./yarn.lock ./yarn.lock
RUN yarn install --dev --frozen-lockfile

# for entry point
COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
