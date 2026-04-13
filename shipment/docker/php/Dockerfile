FROM dunglas/frankenphp:1-php8.3
USER root
RUN apt-get update && apt-get install -y git curl libpng-dev libonig-dev libxml2-dev zip unzip postgresql-client && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN install-php-extensions pdo_pgsql pgsql gd intl zip opcache
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer
WORKDIR /app
COPY . .
RUN composer install --no-interaction --optimize-autoloader && php artisan package:discover --ansi
# Match container user to your host UID/GID
ARG USER_ID=1000
ARG GROUP_ID=1000
RUN if [ $(id -u) != 0 ]; then \
    groupmod -o -g $GROUP_ID www-data && \
    usermod -o -u $USER_ID www-data; \
    fi && \
    chown -R www-data:www-data /app/storage /app/bootstrap/cache /app/vendor
USER www-data
EXPOSE 80 443
CMD ["frankenphp", "run", "--config", "/app/docker/php/Caddyfile"]
