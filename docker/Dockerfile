FROM debian:bookworm-slim
ARG GH_RUNNER_VERSION=2.294.0

ARG COMMIT_SHA=main

ENV RUNNER_NAME=""
ENV GITHUB_SERVER=""
ENV GITHUB_TOKEN=""
ENV RUNNER_LABELS=""
ENV RUNNER_OPTIONS=""
ENV RUNNER_WORK_DIRECTORY="_work"
ENV RUNNER_ALLOW_RUNASROOT=false
ENV AGENT_TOOLS_DIRECTORY=/opt/hostedtoolcache

ENV ANSIBLE_STRATEGY_PLUGINS=/usr/local/lib/python3.10/dist-packages/ansible_mitogen/plugins/strategy
ENV ANSIBLE_STRATEGY=mitogen_linear
RUN /bin/true \
  && apt-get update \
  && apt-get -y install --no-install-recommends \
      openssh-client="*" \
      bind9-dnsutils="*" \
      curl="*" \
      jq="*" \
      git="*" \
      python3.9="*" \
      python3-poetry="*" \
      python3-cachecontrol="*" \
      gpg="*" \
      gpg-agent="*" \
      docker.io="*" \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
WORKDIR /
COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml
RUN /bin/true\
    && /usr/bin/poetry config virtualenvs.create false \
    && poetry install --no-interaction \
    && rm -rf /root/.cache/pypoetry

RUN useradd -m actions && mkdir -p /home/actions ${AGENT_TOOLS_DIRECTORY}
WORKDIR /home/actions
RUN /bin/true \
    && curl -L -O https://github.com/actions/runner/releases/download/v${GH_RUNNER_VERSION}/actions-runner-linux-x64-${GH_RUNNER_VERSION}.tar.gz \
    && tar -zxf actions-runner-linux-x64-${GH_RUNNER_VERSION}.tar.gz \
    && rm -f actions-runner-linux-x64-${GH_RUNNER_VERSION}.tar.gz \
    && ./bin/installdependencies.sh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN /bin/true \
    && cp bin/runsvc.sh . \
    && chmod +x ./runsvc.sh

COPY entrypoint.sh .
RUN chmod +x ./entrypoint.sh
RUN chown -R actions:actions /home/actions ${AGENT_TOOLS_DIRECTORY}

USER actions
CMD [ "./entrypoint.sh" ]
