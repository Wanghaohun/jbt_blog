# Ubuntu 14.04，Trusty Tahr（可靠的塔尔羊）发行版
FROM daocloud.io/ubuntu:14.04

# Me出品
MAINTAINER Me <support@daocloud.io>
COPY 'sources.list' '/etc/apt/sources.list'

# APT 自动安装 Python 相关的依赖包，如需其他依赖包在此添加
RUN apt-get update 
RUN apt-get -y install python3 
RUN apt-get -y install python3-pip  
RUN apt-get -y install git

ADD http://nginx.org/download/nginx-1.9.15.tar.gz
RUN tar zxvf nginx-1.9.15.tar.gz .
RUN mkdir -p /usr/local/nginx
RUN cd nginx-1.9.15 && ./configure --prefix=/usr/local/nginx && make && make install
RUN rm -vf /usr/local/nginx/conf/nginx.conf
COPY 'nginx.conf' '/usr/local/nginx/conf/nginx.conf'
# 用完包管理器后安排打扫卫生可以显著的减少镜像大小
RUN apt-get clean \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* 
    
# 配置默认放置 App 的目录
RUN mkdir -p /app
WORKDIR /app

#克隆项目到文件夹
RUN git clone https://github.com/Wanghaohun/jbt_blog.git
#安装所需库
WORKDIR /app/jbt_blog
RUN mkdir /app/jbt_blog/jbt_blog/log
RUN mkdir /app/jbt_blog/jbt_blog/log/nginx
RUN touch /app/jbt_blog/jbt_blog/log/nginx/access.log
RUN touch /app/jbt_blog/jbt_blog/log/nginx/error.log
RUN pip3 install ipython
RUN pip3 install -Ur requirements.txt
RUN pip3 install gunicorn
RUN nginx -t
RUN service nginx restart
CMD ["/bin/bash"] #gunicorn -w 3 -b 0.0.0.0:8000 jbt_blog.wsgi:application

# PORT 端口映射设置
EXPOSE 8000
EXPOSE 443
EXPOSE 80