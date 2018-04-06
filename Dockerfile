FROM adsabs/base-microimage

# add scripts/tags
ADD repository /repository
ADD release /release

WORKDIR /app
RUN /bin/bash -c "git clone `cat /repository` /app"
RUN git pull && git reset --hard `cat /release`

# Provision the project
RUN pip install -r requirements.txt

EXPOSE 80
# insert the local config
ADD local_config.py /local_config.py
RUN /bin/bash -c "find . -maxdepth 2 -name config.py -exec /bin/bash -c 'echo {} | sed s/config.py/local_config.py/ | xargs -n1 cp /local_config.py' \;"
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
