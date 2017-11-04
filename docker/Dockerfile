FROM debian:jessie
LABEL Maintainer1="Ning <ning@stensalinc.com>"

RUN apt-get update
RUN apt-get install -y nginx-full \
    && apt-get install -y php5 php5-fpm php5-cgi php5-xdebug php5-curl php5-mysql

COPY bin/cppcms_api.so /usr/lib/php5/20131226/
COPY cppcms_api.ini /etc/php5/mods-available/
RUN  cd /etc/php5/fpm/conf.d \
     && ln -s ../../mods-available/cppcms_api.ini 30-cppcms_api.ini

COPY php.nginx /etc/nginx/sites-enabled/
COPY php.ini /etc/php5/fpm/php.ini

COPY wwwtest/ /var/www/html/
COPY phpbb/   /var/www/html/forum/
RUN mkdir -p /var/www/html/forum/cache/production \
    && chown -R www-data:www-data /var/www/html/forum/cache/production

VOLUME /var/www/html/forum

ENTRYPOINT nginx && service php5-fpm start && /bin/bash

CMD ["true"]

EXPOSE 8000
