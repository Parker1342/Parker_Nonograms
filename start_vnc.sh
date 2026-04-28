#!/bin/bash

# Kill old displays
pkill Xvfb
pkill x11vnc

# Start a virtual display
Xvfb :1 -screen 0 1280x800x24 &

# Start VNC server on top of that display
x11vnc -display :1 -nopw -forever -shared &

# Start WebSocket proxy on port 9000
websockify --web=/usr/share/novnc/ \
  --wrap-mode=ignore \
  0.0.0.0:9000 \
  localhost:5900
