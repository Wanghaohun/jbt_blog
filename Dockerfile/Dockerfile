# Ubuntu 14.04，Trusty Tahr（可靠的塔尔羊）发行版
FROM daocloud.io/ubuntu:14.04

# Dockerfile Author:Wanghaohun 
MAINTAINER Wanghaohun <hornewang@gmail.com>
COPY 'sources.list' '/etc/apt/sources.list'

# APT 自动安装 Python 相关的依赖包，如需其他依赖包在此添加
RUN apt-get update 
RUN apt-get -y install python3 
RUN apt-get -y install python3-pip  
RUN apt-get -y install git

# APT 自动安装 Nginx 相关的依赖包，如需其他依赖包在此添加
RUN apt-get -y install openssl libssl-dev
RUN apt-get -y install libpcre3 libpcre3-dev
RUN apt-get -y install zlib1g-dev
# 配置默认放置 App 的目录
RUN mkdir -p /app
WORKDIR /app
COPY 'nginx-1.9.15.tar.gz' '/app/nginx-1.9.15.tar.gz'
RUN tar -zxvf /app/nginx-1.9.15.tar.gz
RUN mkdir -p /usr/local/nginx
WORKDIR /app/nginx-1.9.15
RUN ./configure --prefix=/usr/local/nginx --with-http_ssl_module&& make && make install
RUN rm -vf /usr/local/nginx/conf/nginx.conf
COPY 'nginx.conf' '/usr/local/nginx/conf/nginx.conf'

# 用完包管理器后安排打扫卫生可以显著的减少镜像大小
RUN apt-get clean \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* 
  
#克隆项目到文件夹
WORKDIR /app
RUN git clone https://github.com/Wanghaohun/jbt_blog.git

#安装项目依赖及新建日志文件
WORKDIR /app/jbt_blog
RUN pip3 install ipython
RUN pip3 install -Ur requirements.txt
RUN pip3 install gunicorn
RUN mkdir /app/jbt_blog/jbt_blog/log
RUN mkdir /app/jbt_blog/jbt_blog/log/nginx
RUN touch /app/jbt_blog/jbt_blog/log/nginx/access.log
RUN touch /app/jbt_blog/jbt_blog/log/nginx/error.log
RUN mkdir /var/log/nginx
RUN touch /var/log/nginx/error.log

CMD ["/bin/bash"] 
#gunicorn -w 3 -b 0.0.0.0:8000 jbt_blog.wsgi:application

# PORT 端口映射设置
EXPOSE 8000
EXPOSE 443
EXPOSE 80