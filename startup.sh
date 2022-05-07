#!/bin/bash

# Create download folder & rclone folder
mkdir -p /app/aria2
mkdir -p ~/.config/rclone

# Creating rclone config file
echo "[upload]
${RCLONE_REMOTE}
" >>~/.config/rclone/rclone.conf

# Starting Rclone RC Server
rclone rcd --rc-no-auth --drive-server-side-across-configs \
  --rc-job-expire-interval=86400s --rc-job-expire-duration=86400s &

# Aria2 RPC Server for downloading
aria2c --enable-rpc --rpc-listen-all=true --rpc-listen-port 6800 \
  --max-connection-per-server=10 --continue=true --split=10 --daemon=true \
  --rpc-save-upload-metadata=false --rpc-max-request-size=1024M --follow-torrent=mem \
  --allow-overwrite=true --max-concurrent-downloads=5 --seed-time=0 --bt-seed-unverified=true \
  --bt-max-peers=0 --bt-tracker-connect-timeout=10 --bt-tracker-timeout=10 \
  --user-agent='qBittorrent v4.3.3' --peer-agent='qBittorrent v4.3.3' --peer-id-prefix=-qB4330- \
  --on-download-complete=/app/on_finish.sh --dir=/app/aria2 &

# Ping Heroku server
if [[ -z "$APP_NAME" ]]; then
  echo "[ ERROR ] APP_NAME is set to the empty string"
else
  echo "[ INFO ] Starting keep alive script..."
  bash keep_alive.sh &
fi

uvicorn src.api:app --host=0.0.0.0 --port="${PORT:-5000}"
