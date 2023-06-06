from pytapo import Tapo
from pytapo.media_stream.downloader import Downloader
import asyncio
import os
from datetime import datetime

# mandatory
outputDir = os.environ.get("OUTPUT")  # directory path where videos will be saved
date = os.environ.get("DATE")  # date to download recordings for in format YYYYMMDD
host = os.environ.get("HOST")  # change to camera IP
password_cloud = os.environ.get("PASSWORD_CLOUD")  # set to your cloud password

# optional
window_size = os.environ.get(
    "WINDOW_SIZE"
)  # set to prefferred window size, affects download speed and stability, recommended: 50


async def download_async():
    print("Connecting to camera...")
    tapo = Tapo(host, "admin", password_cloud, password_cloud)
    print("Getting recordings...")
    recordings = tapo.getRecordings(date)
    for recording in recordings:
        for key in recording:
            startTime = recording[key]["startTime"]
            endTime = recording[key]["endTime"]
            dateStart = datetime.utcfromtimestamp(int(startTime)).strftime("%Y%m%d_%H%M%S")
            dateEnd = datetime.utcfromtimestamp(int(endTime)).strftime("%H%M%S")
            fileName = dateStart + "_" + dateEnd + ".mp4"

            downloader = Downloader(
                tapo,
                startTime,
                endTime,
                outputDir,
                None,
                False,
                window_size,
                fileName,
            )
            async for status in downloader.download():
                statusString = status["currentAction"] + " " + status["fileName"]
                if status["progress"] > 0:
                    statusString += (
                        ": "
                        + str(round(status["progress"], 2))
                        + " / "
                        + str(status["total"])
                    )
                else:
                    statusString += "..."
                print(
                    statusString + (" " * 10) + "\r", end="",
                )
            print("")


loop = asyncio.get_event_loop()
loop.run_until_complete(download_async())

