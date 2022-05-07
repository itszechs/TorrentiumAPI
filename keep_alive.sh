COUNT=1
SERVER_URL="http://${APP_NAME}.herokuapp.com"

while true; do
  STATUS_CODE=$(curl -Is "$SERVER_URL" | grep HTTP | cut -d ' ' -f2)
  echo "[ INFO ] SERVER PINGED $COUNT. $SERVER_URL - $STATUS_CODE"
  COUNT=$((COUNT + 1))
  sleep 600
done
