from OpenSubtitles import OpenSubtitles
import pandas as pd
from tqdm import tqdm
import requests
import os 

def get_imdb_ids():
    data=pd.read_csv("data/OpenSubtitles_file_ids.csv")
    data=data[["imdb_id","file_id"]]

    files=os.listdir("subtitles/")
    files=[i[:9] for i in files]
    return list(data[~ data.imdb_id.isin(files)].iterrows())


if __name__ =="__main__":
    username=""
    password=""
    api_key=""

    open_subtitles= OpenSubtitles(username,password,api_key)

    for _, row in tqdm(get_imdb_ids()):
        response= open_subtitles.download_subtitles_with_file_id(row.file_id)
        if response["remaining"]>-1:
            link,file_name=response["link"], response["file_name"]

            #downloading subtitle file
            response=requests.get(link)
            open("subtitles/"+str(row.imdb_id)+"_subtitle", "w", encoding="utf-8").write(response.content.decode())
        else:
            print("Download Limit reached!")
            break
