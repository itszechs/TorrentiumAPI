# TorrentiumAPI

The backend for the [Torrentium](https://github.com/itsZECHS/TorrentiumApp) Android app.

## Features

- **RESTful** - The RESTful API is built using the [FastAPI](https://fastapi.tiangolo.com/) framework
- **Scraper** - API to torrents site such as [nyaa.si](https://nyaa.si/) and [sukebei.nyaa.si](https://sukebei.nyaa.si/)
- **Caching** - The server is configured cache the results for 2 minutes.
- **All-purpose downloader** - Access to [aria2c](https://aria2.github.io/) for downloading torrents
- **Automated uploads** - Automated uploads of downloads via [rclone](https://rclone.org/) to cloud storage.

## Deploy on heroku

```bash
git clone https://github.com/itsZECHS/TorrentiumAPI.git
cd TorrentiumAPI
heroku create
heroku stack:set container -a {app_name}
heroku git:remote -a {app_name}
git push heroku main
```

## Set environment variables

![Heroku Config Vars](https://files.catbox.moe/3x6bb7.png)

- Here `RCLONE_TOKEN` is the token from rclone config, to obtain this follow steps below

```bash
rclone config show
```

![What to copy](https://files.catbox.moe/32ujgg.png)

Copy the `token` value from the output.

- The `TEAM_DRIVE_ID` is the id of the team drive where you want to store your downloads.

You can copy this from the output of `rclone config show` (above) or Google Drive's team drive page.

## How to use?

Once deployed, you can vist [localhost](http://127.0.0.1:5000/redoc) for full documentation on the api.

The intended use of this API is to be used by the Torrentium app which you can download from [here](https://github.com/itsZECHS/TorrentiumApp/releases).

## Demo

Check out the publicly deployed version here [Heroku - TorrentiumAPI](https://torrentium-api.herokuapp.com/redoc).

This is only for demonstration purpose and is not intended to be used in production.
