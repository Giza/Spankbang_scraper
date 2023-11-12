# 12.11.2023

# Import
import requests, sys
from rich.console import Console
from bs4 import BeautifulSoup
from seleniumbase import Driver

# Variable
console = Console()
url = input("INSERT URL => ").replace(" ", "")


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

console.log("[green]Save video")
title = url.split("/")[-1].replace("+", "_").replace("?", "").replace("!", "").replace(",", "")
open(title + ".mp4", "wb").write(requests.get(video_url).content)

console.log("[red]End")
sys.exit(0)