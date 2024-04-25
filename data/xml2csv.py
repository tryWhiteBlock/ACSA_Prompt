import xml.etree.ElementTree as ET
import pandas as pd
def toCsv_mams(src:str,target:str):
    tree=ET.parse(src)
    root=tree.getroot()
    sentences=tree.findall("sentence")
    polarities=["neutral","positive","negative"]
    data=[]
    for sentence in sentences:
        dic={}
        dic["sentence"]=sentence.find("text").text
        aspects=sentence.find("aspectCategories").findall("aspectCategory")
        for aspect in aspects:
            if aspect.get("polarity") is None:
                dic[aspect.get("category")]=None
                continue
            dic[aspect.get("category")]=polarities.index(aspect.get("polarity"))
        data.append(dic)
    data=pd.DataFrame(data)
    data.to_csv(target,index=False)

def toCsv_14(src:str,target:str):
    tree=ET.parse(src)
    root=tree.getroot()
    sentences=tree.findall("sentence")
    polarities=["neutral","positive","negative"]
    data=[]
    for sentence in sentences:
        dic={}
        dic["sentence"]=sentence.find("text").text
        aspects=sentence.find("aspectCategories").findall("aspectCategory")
        for aspect in aspects:
            if aspect.get("polarity") is None or aspect.get("polarity").__eq__("conflict"):
                dic[aspect.get("category")]=None
                continue
            dic[aspect.get("category")]=polarities.index(aspect.get("polarity"))
        data.append(dic)
    data=pd.DataFrame(data)
    data.to_csv(target,index=False)

if __name__ == "__main__":
    src="/home/su/acsa_prompt/data/origin_data/14_test.xml"
    target="/home/su/acsa_prompt/data/processed_data/14_test.csv"
    toCsv_14(src,target)

