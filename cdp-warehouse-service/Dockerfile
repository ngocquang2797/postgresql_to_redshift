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

RUN apt-get -y install openvpn
RUN service openvpn restart
#COPY vpn/setel-datateam-client-config.ovpn /setel-datateam-client-config.ovpn
#RUN openvpn --config setel-datateam-client-config.ovpn  --auth-user-pass "paul-FnRb7fV44xTtB8fmbL5Zk5Zw7-253596" --auth-retry interact

ENV POSTGRES_URI="postgres:abcd1234@golangvietnam.com:5432"

ENV POSTGRES_NAME="dev-metadata"

ENV POSTGRES_NAME_TRANSFORM="dev-transformdata"

ENV RDS_URI="{user}:{pass}@{host}:{port}"

ENV RDS_NAME="dev"

# expose port 3001 on the vm
EXPOSE 3001

# run `npm start` to setup the server
WORKDIR /cdp-warehouse-service/cdp-warehouse-service
CMD ["python", "server.py"]