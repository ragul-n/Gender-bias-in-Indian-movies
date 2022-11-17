from OpenSubtitles import OpenSubtitles
import pandas as pd

def get_subtitle_file_id(imdb_ids):
    sub_file_data=[]

    for id in imdb_ids:
        file_id, file_attr=os.get_subtitle_file_id(id[2:], additional_attributes=['from_trusted', 'ai_translated','machine_translated',"language"])
        if file_id !=None:
            file_attr=dict(file_attr)
            file_attr["file_id"]=file_id
            file_attr["imdb_id"]=id
            sub_file_data.append(file_attr)
            
        else:
            sub_file_data.append({"imdb_id":id})

        return sub_file_data

if __name__ =="__main__":
    username=""
    password=""
    api_key=""

    os= OpenSubtitles(username,password,api_key)

    movies_data= pd.read_csv("https://raw.githubusercontent.com/ragul-n/Gender-bias-in-Indian-cinema/master/indian%20movies.csv")
    imdb_ids=movies_data.ID

    sub_file_ids=get_subtitle_file_id(imdb_ids)
    
    df=pd.DataFrame(sub_file_ids)
    df.to_csv("subtitle_file_ids.csv",index=False)
