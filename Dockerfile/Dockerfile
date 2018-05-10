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
RUN pip3 install -Ur requirements.txt
CMD ["/bin/bash"]

# PORT 端口映射设置
EXPOSE 8000