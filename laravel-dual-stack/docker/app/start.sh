#!/bin/sh
set -e

APP_DIR=/var/www

mkdir -p $APP_DIR/storage \
         $APP_DIR/storage/framework \
         $APP_DIR/storage/framework/cache \
         $APP_DIR/storage/framework/sessions \
         $APP_DIR/storage/framework/views \
         $APP_DIR/storage/logs \
         $APP_DIR/bootstrap/cache

if [ -f "$APP_DIR/composer.json" ]; then
    composer install --no-interaction --prefer-dist || true
fi

if [ -f "$APP_DIR/.env.example" ] && [ ! -f "$APP_DIR/.env" ]; then
    cp "$APP_DIR/.env.example" "$APP_DIR/.env"
fi

if [ -f "$APP_DIR/.env" ]; then
    sed -i "s|^APP_NAME=.*|APP_NAME=\"${APP_NAME}\"|g" "$APP_DIR/.env" || true
    sed -i "s|^APP_ENV=.*|APP_ENV=${APP_ENV}|g" "$APP_DIR/.env" || true
    sed -i "s|^APP_DEBUG=.*|APP_DEBUG=${APP_DEBUG}|g" "$APP_DIR/.env" || true
    sed -i "s|^APP_URL=.*|APP_URL=${APP_URL}|g" "$APP_DIR/.env" || true

    sed -i "s|^DB_CONNECTION=.*|DB_CONNECTION=${DB_CONNECTION}|g" "$APP_DIR/.env" || true
    sed -i "s|^DB_HOST=.*|DB_HOST=${DB_HOST}|g" "$APP_DIR/.env" || true
    sed -i "s|^DB_PORT=.*|DB_PORT=${DB_PORT}|g" "$APP_DIR/.env" || true
    sed -i "s|^DB_DATABASE=.*|DB_DATABASE=${DB_DATABASE}|g" "$APP_DIR/.env" || true
    sed -i "s|^DB_USERNAME=.*|DB_USERNAME=${DB_USERNAME}|g" "$APP_DIR/.env" || true
    sed -i "s|^DB_PASSWORD=.*|DB_PASSWORD=${DB_PASSWORD}|g" "$APP_DIR/.env" || true

    if grep -q '^DB_PREFIX=' "$APP_DIR/.env"; then
        sed -i "s|^DB_PREFIX=.*|DB_PREFIX=${DB_PREFIX}|g" "$APP_DIR/.env" || true
    else
        echo "DB_PREFIX=${DB_PREFIX}" >> "$APP_DIR/.env"
    fi
fi

if [ -f "$APP_DIR/artisan" ]; then
    php artisan key:generate --force || true
    php artisan config:clear || true
    php artisan cache:clear || true
    php artisan config:cache || true
fi

chown -R ${LOCAL_UID}:${LOCAL_GID} $APP_DIR
chmod -R ug+rwX $APP_DIR/storage $APP_DIR/bootstrap/cache || true

exec php-fpm
