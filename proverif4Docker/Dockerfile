FROM alpine:3.11.0
# Install Python3
RUN apk update && apk add python3
# Install Flask-Restful
RUN python3 -m pip install flask && python3 -m pip install flask-restful
# Install some Packages (needed for ProVerif's installation)
RUN apk update && apk add make m4 ocaml-compiler-libs libc-dev gcc
RUN apk add --update --no-cache ttf-freefont && apk add ghostscript
# Install Proverif
RUN apk update && apk add opam && opam init -ya --disable-sandboxing
RUN opam install -y depext
RUN opam depext -y conf-graphviz && opam depext -y proverif && opam install -y proverif

# Creation of some useful directory
RUN mkdir -p /proverifdata/api \
 && mkdir -p /proverifdata/script \
 && mkdir -p /proverifdata/css \
 && mkdir -p /models

EXPOSE 5001

# Add CSS for proverif html
COPY cssproverif.css /proverifdata/css/
# Add Api File
COPY api.py /proverifdata/api/
# Add Scripts File
COPY runproverif.sh  /proverifdata/script/
COPY startflask.sh /
RUN chmod 755 /startflask.sh && chmod 755 /proverifdata/script/runproverif.sh

CMD ["/startflask.sh"] 





# ProVerif location => /root/.opam/default/bin
# $ docker build . -t proverif4docker
# $ docker run -ti -d --publish 8080:5000 --name proverif_server proverif4docker