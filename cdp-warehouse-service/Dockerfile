# Create builder
FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean

RUN pip install --upgrade pip

COPY requirement.txt /requirement.txt
RUN pip install -r requirement.txt

#COPY ./server.py /app
#COPY ./internal /app/internal

RUN apt-get -y install openvpn
RUN service openvpn restart
COPY vpn/setel-datateam-client-config.ovpn /setel-datateam-client-config.ovpn
#RUN openvpn --config setel-datateam-client-config.ovpn

## Main Image
#FROM python:3.8.0-slim as app
#COPY --from=builder /root/.local /root/.local
#COPY --from=builder /app /app
#WORKDIR /app
#ENV PATH=/root/.local/bin:$PATH

# expose port 3001 on the vm
EXPOSE 3001

# run `npm start` to setup the server
WORKDIR /cdp-warehouse-service/cdp-warehouse-service
#CMD [ "python", "server.py" ]