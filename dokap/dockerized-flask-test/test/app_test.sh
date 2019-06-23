#!/usr/bin/env bash
APP_URL="app"
APP_PORT="5000"

function get_http_response {
    curl -L --write-out %{http_code} --silent --output /dev/null $1
}

while [[ $(get_http_response ${APP_URL}:${APP_PORT}) != "200" ]]; do
    echo "waiting..."
    sleep 1
done

echo "OK"
