#!/bin/sh

# $1 is gid.
# $2 is the number of files.
# $3 is the path of the first file.

if [ "$2" = "0" ]; then
    echo "$(date)" "INFO  no file to move for" "$1"
    exit 0
fi

while true; do

    MONTH_YEAR_FOLDER=$(date +'%B - %Y')
    DOWNLOAD_NAME=$(echo "$3" | cut -d'/' -f4)
    SOURCE_PATH=$(echo "$3" | cut -d'/' -f-4)

    echo "SOURCE_PATH=$SOURCE_PATH"

    if [ -d "${SOURCE_PATH}" ]; then
        echo "$(date)" "INFO " "$SOURCE_PATH" moved as "$DOWNLOAD_NAME"
        DESTINATION="${MONTH_YEAR_FOLDER}/Folders/${DOWNLOAD_NAME}"

        rclone rc sync/move \
            srcFs="${SOURCE_PATH}" \
            dstFs="upload:/${DESTINATION}" \
            _async="true" deleteEmptySrcDirs="true"

        exit $?
    elif [ -f "${SOURCE_PATH}" ]; then
        echo "$(date)" "INFO: " "$3" moved as "$DOWNLOAD_NAME"
        DESTINATION="${MONTH_YEAR_FOLDER}/Files/${DOWNLOAD_NAME}"

        rclone rc operations/movefile \
            srcFs="/app/aria2" \
            srcRemote="${DOWNLOAD_NAME}" \
            dstFs="upload:" \
            dstRemote="/${DESTINATION}" \
            _async="true"

        exit $?
    else
        echo "well, if it is not a file or a folder then it probably doesn't exist"
    fi
done
