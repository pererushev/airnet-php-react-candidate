FROM php:7.4-cli-bullseye
# 1. Перенаправляем все запросы на архивный сервер
# 2. Убираем репозиторий updates, так как в архиве он не нужен и вызывает ошибки
RUN sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    sed -i 's|security.debian.org|archive.debian.org|g' /etc/apt/sources.list && \
    sed -i '/bullseye-updates/d' /etc/apt/sources.list
RUN apt-get update && apt-get install -y --no-install-recommends --fix-missing libpq-dev && docker-php-ext-install pgsql && rm -rf /var/lib/apt/lists/*
WORKDIR /app
ENV PHP_CLI_SERVER_WORKERS=4
CMD ["php", "-d", "display_errors=0", "-S", "0.0.0.0:8080", "-t", "public", "public/router.php"]
