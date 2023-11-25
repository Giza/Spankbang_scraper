# 25.11.2023

import requests
import sys
from rich.console import Console
from bs4 import BeautifulSoup
from seleniumbase import Driver

# Function to process a single URL
console = Console()
def process_url(url):
    console.log("[green]Get driver")
    driver = Driver(uc=True, headless=True)
    driver.get(url)

    console.log("[green]Get page")
    r_text = driver.page_source
    soup = BeautifulSoup(r_text, "lxml")

    console.log("[green]Find url")
    video_url = ""
    for video in soup.find_all("video"):
        video_url = video.get("src")
        if "blob" not in video_url and "gallery" not in video_url:
            break

    driver.quit()

    if video_url:
        try:
            console.log("[green]Save video")
            title = url.split("/")[3].replace("+", "_").replace("?", "").replace("!", "").replace(",", "")+"_"+url.split("/")[-1].replace("+", "_").replace("?", "").replace("!", "").replace(",", "")
            open(title + ".mp4", "wb").write(requests.get(video_url).content)
        except Exception as e:
            console.log("[red]Error saving video:", str(e))
    else:
        console.log("[yellow]No video URL found for:", url)

    console.log("[red]End")

# Read URLs from a text file
with open("urls.txt", "r") as file:
    urls = file.read().splitlines()

# Process each URL
for url in urls:
    print(url)
    process_url(url)

sys.exit(0)
