# Ahri Secrecy

## Encryption by HTTP request. MD5, SHAx, RSA, AES, DES, etc.

## Build the image

```Dockerfile
FROM python:3.8
MAINTAINER "ahri"<ahriknow@ahriknow.cn>
ADD app.py /project/app.py
ADD requirements.txt /project/requirements.txt
ADD pip.conf /etc/pip.conf
WORKDIR /project
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 9000
ENTRYPOINT ["gunicorn", "-w", "2", "-b", "0.0.0.0:9000", "app:app"]
```

## Run a container

```bash
docker container run --name secrecy -p 80:9000 -d ahriknow/secrecy:v20200320
```

-   `--name secrecy` 容器名为 secrecy
-   `-p 80:9000` 将容器 9000 端口映射到宿主机 80 端口
-   `-d` 后台运行
-   `ahriknow/secrecy:v20200320` 镜像

## Python requirements.txt

```
pycertifi==2019.11.28
chardet==3.0.4
click==7.1.1
Flask==1.1.1
idna==2.9
itsdangerous==1.1.0
Jinja2==2.11.1
MarkupSafe==1.1.1
Naked==0.1.31
pycryptodome==3.9.7
PyYAML==5.3.1
requests==2.23.0
shellescape==3.8.1
urllib3==1.25.8
Werkzeug==1.0.0
```

## How to use

-   `GET http://ip:port/secrecy/?<option>=<args>&...`
-   `POST http://ip:port/secrecy/` Content-Type: application/json

```json
{
	"type": "",
	"text": ""
}
```

| key  | value                                                                                                                     | explain    |
| ---- | ------------------------------------------------------------------------------------------------------------------------- | ---------- |
| type | md5、sha1、sha224、sha256、sha384、sha512、sha3_224、sha3_256、sha3_384、sha3_512、blake2b、blake2s、shake_128、shake_256 | 加密方式   |
| text | ""                                                                                                                        | 待加密文本 |

-   `GET http://ip:port/secrecy/?<option>=<args>&...`
-   `POST http://ip:port/secrecy/` Content-Type: application/json

```json
{
	"type": "",
	"key": "",
	"text": ""
}
```

| key  | value                           | explain                      |
| ---- | ------------------------------- | ---------------------------- |
| type | AES,D-AES,DES,D-DES,DES3,D-DES3 | 加密方式 ,D-: 解密           |
| key  | ""                              | 密钥,AES<=32,DES<=8,DES3<=16 |
| text | ""                              | 待加密文本                   |

-   `POST http://ip:port/secrecy/` Content-Type: application/json

```json
{
	"type": "",
	"password": "生成密钥包含 password, 则 加解密 必传",
	"text": "",
	"pub_k": "加密 必传",
	"pri_k": "解密 必传"
}
```

| key            | value             | explain                       |
| -------------- | ----------------- | ----------------------------- |
| type           | rsa-k,rsa-e,rsa-d | -k:生成密钥对,-e:加密,-d:解密 |
| password(可选) | ""                | 密码,为空则不设               |
| text           | ""                | 待 加密/解密 文本             |
| pub_k          | ""                | 加密密钥                      |
| pri_k          | ""                | 解密密钥                      |

## Powered By ahri 20200320
