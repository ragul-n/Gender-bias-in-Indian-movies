import requests
import pandas as pd



class OpenSubtitles:

    # Wrapper for OpenSubtitles API

    def __init__(self, username, password, api_key):
        self.username= username
        self.password= password
        self.api_key= api_key
        self.login()

    def login(self):
        headers ={
            'Api-key': self.api_key,
            'Content-Type': 'application/json',
            }
            
        data = str({"username":self.username,"password":self.password})



        response = requests.post('https://api.opensubtitles.com/api/v1/login',headers=headers, data=data )
        #return response.json()["token"]

    
    def search_subtitles(self, params):
        headers = {
            'Api-Key': self.api_key,
        }

        print(params)
        response = requests.get('https://api.opensubtitles.com/api/v1/subtitles', headers=headers, params=params)
        print(response.json())
        return response.json()["data"]
    
    def download_subtitles_with_file_id(self, file_id):
        headers = {
            'Api-key': self.api_key,
        }


        data={"file_id":int(file_id)}

        response= requests.post("https://api.opensubtitles.com/api/v1/download", headers=headers, data=data)
        print(response)
        return response.json()

    def download_subtitle_with_imdb_id(self, imdb_id, language="en"):
        
        files=self.search_subtitles(params = (
                            ("machine_translated","False"),
                            ("ai_translated","False"),
                            ("language",language),
                            ('imdb_id', imdb_id),
                        ))
        
        subtitles= pd.DataFrame([file['attributes'] for file in files])
        subtitles=subtitles[subtitles["language"]==language]

        file_id= subtitles.iloc[0].files[0]["file_id"]
        response=self.download_subtitles_with_file_id(file_id)
        link,file_name=response["link"], response["file_name"]

        #downloading subtitle file
        response=requests.get(link)
        open(file_name, "w").write(response.content.decode())

        return file_name


if __name__ =="__main__":
    username=""
    password=""
    api_key=""

    os= OpenSubtitles(username,password,api_key)

    filename= os.download_subtitle_with_imdb_id("5200962") # 5200962 -> IMDB Id of Kadhalum Kadandhu Pogum movie
    


