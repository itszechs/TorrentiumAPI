# TorrentiumAPI

The backend for the [Torrentium](https://github.com/itsZECHS/TorrentiumApp) Android app.

## Features

- **RESTful** - The RESTful API is built using the [FastAPI](https://fastapi.tiangolo.com/) framework
- **Scraper** - API to torrents site such as [nyaa.si](https://nyaa.si/) and [sukebei.nyaa.si](https://sukebei.nyaa.si/)
- **Caching** - The server is configured cache the results for 2 minutes.
- **All-purpose downloader** - Access to [aria2c](https://aria2.github.io/) for downloading torrents
- **Automated uploads** - Automated uploads of downloads via [rclone](https://rclone.org/) to cloud storage.

## Deploy on heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/itsZECHS/TorrentiumAPI)

Required tools

- [git](https://git-scm.com/downloads)
- [heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)

```bash
git clone https://github.com/itsZECHS/TorrentiumAPI.git
cd TorrentiumAPI
heroku create
heroku stack:set container -a {app_name}
heroku git:remote -a {app_name}
git push heroku main
```

## Set environment variables

![Heroku Config Vars](https://files.catbox.moe/a9ej8a.png)

- Here `RCLONE_REMOTE` is the token from rclone config, to obtain this follow steps below

- `rclone config show`

![What to copy](https://files.catbox.moe/btobgz.png)

- Copy all config variables (except the remote name).

To avoid your app from sleeping (if you're on free dyno) you can set the `APP_NAME` variable, this should be same as
your heroku app name.

## How to use?

Once deployed, you can vist [localhost](http://127.0.0.1:5000/redoc) for full documentation on the api.

The intended use of this API is to be used by the Torrentium app which you can download
from [here](https://github.com/itsZECHS/TorrentiumApp/releases).

## Demo

Check out the publicly deployed version here [Heroku - TorrentiumAPI](https://torrentium-api.herokuapp.com/redoc).

This is only for demonstration purpose and is not intended to be used in production.
