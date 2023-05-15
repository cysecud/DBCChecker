FROM alpine:3.15.0
# Install Python3 and Java
RUN apk update \
    && apk add python3 \
    # && apk add openjdk14 --repository=http://dl-cdn.alpinelinux.org/alpine/edge/testing
    && apk add openjdk14 \
    && apk add py3-pip

# Install Flask-Restful
RUN python3 -m pip install flask==1.1.4 \
    && python3 -m pip install flask-restful==0.3.9 \
    && python3 -m pip install flask-cors==3.0.10 \
    && python3 -m pip install markupsafe==2.0.1

# Creation of some useful directory
RUN mkdir -p /api \
    && mkdir -p /proverif

EXPOSE 5000
EXPOSE 5001

# Add Api File
COPY api.py /api/
COPY serverProverif-1.1.0.jar /proverif/
# Add Scripts File
COPY startflask.sh /
RUN chmod 755 /startflask.sh

CMD ["/startflask.sh"] 