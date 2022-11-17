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
        
        response = requests.get('https://api.opensubtitles.com/api/v1/subtitles', headers=headers, params=params)
       
        return response.json()["data"]
    
    def download_subtitles_with_file_id(self, file_id):
        headers = {
            'Api-key': self.api_key,
        }


        data={"file_id":int(file_id)}

        response= requests.post("https://api.opensubtitles.com/api/v1/download", headers=headers, data=data)
      
        return response.json()

    def get_subtitle_file_id(self,imdb_id, language="en", additional_attributes =[]):
        files=self.search_subtitles(params = (
                            ("machine_translated","False"),
                            ("ai_translated","False"),
                            ("language",language),
                            ('imdb_id', imdb_id),
                        ))
        
        subtitles= pd.DataFrame([file['attributes'] for file in files])
        if len(subtitles) !=0:
            subtitles=subtitles[subtitles["language"]==language]
            if len(subtitles)==0: return None, None
            
            try:    
                file_id= subtitles.iloc[0].files[0]["file_id"]
            except:
                print(subtitles)
                print("len",len(subtitles))
            file_attributes= subtitles.iloc[0][additional_attributes]  if (len(additional_attributes)>0) else None

            return file_id, file_attributes
        else:
            return None, None

    def download_subtitle_with_imdb_id(self, imdb_id, language="en"):
        """
        Downloads the subtitles 
        """
        file_id, _ = self.get_subtitle_file_id(imdb_id, language=language)
        if file_id != None:
            response=self.download_subtitles_with_file_id(file_id)
            link,file_name=response["link"], response["file_name"]

            #downloading subtitle file
            response=requests.get(link)
            open(str(imdb_id)+"_subtitle", "w").write(response.content.decode())

            return file_name
        else:
            return None


if __name__ =="__main__":
    username=""
    password=""
    api_key=""

    os= OpenSubtitles(username,password,api_key)

    filename= os.download_subtitle_with_imdb_id("5200962") # 5200962 -> IMDB Id of Kadhalum Kadandhu Pogum movie
    


