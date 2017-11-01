FROM debian:jessie
LABEL Maintainer1="Ning <ning@stensalinc.com>"

RUN apt-get update
RUN apt-get install -y nginx-full \
    && apt-get install -y php5 php5-fpm php5-cgi php5-xdebug php5-mysql

COPY bin/cppcms_api.so /usr/lib/php5/20131226/
COPY cppcms_api.ini /etc/php5/mods-available/
RUN  cd /etc/php5/fpm/conf.d \
     && ln -s ../../mods-available/cppcms_api.ini 30-cppcms_api.ini

COPY php.nginx /etc/nginx/sites-enabled/

COPY wwwtest/ /var/www/html/
COPY phpbb/   /var/www/html/forum/
RUN mkdir -p /cache/production \
    && chown -R www-data:www-data /cache/production

COPY entrypoint.sh /usr/bin/entrypoint.sh 

ENTRYPOINT ["/usr/bin/entrypoint.sh"]
