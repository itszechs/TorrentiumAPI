count=1
while true ; 
    do 
        if [[ ! -v SERVER_URL ]]; then
            echo "[ ERROR ] SERVER_URL is not set"
        elif [[ -z "$SERVER_URL" ]]; then
            echo "[ ERROR ] SERVER_URL is set to the empty string"
        else
            x=$(curl -s $SERVER_URL); 
            echo "[ INFO ] Ping SERVER - $count -  : $SERVER_URL"
            count=$(($count+1))
        fi
        
        # ping server after every 10 min
        sleep 600 ;
        
done