#!/bin/bash
export DISPLAY=:99
Xvfb :99 -screen 0 1024x768x16 &
sleep 1
x11vnc -display :99 -forever -shared -noxdamage -rfbport 5900 &
while ! nc -z localhost 5900; do sleep 1; done
cd /app/noVNC
./utils/novnc_proxy --vnc localhost:5900 --listen 0.0.0.0:6080
exec "$@"