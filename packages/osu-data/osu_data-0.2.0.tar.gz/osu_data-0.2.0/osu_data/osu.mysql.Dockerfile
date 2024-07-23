FROM mysql

COPY osu.mysql.healthcheck.sh /osu.mysql.healthcheck.sh
COPY osu.mysql.cnf /etc/mysql/my.cnf

RUN ["chmod", "+x", "/osu.mysql.healthcheck.sh"]