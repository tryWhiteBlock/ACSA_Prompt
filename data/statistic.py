import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn
def data_distribution(src:str,target:str):
    polarities=["neutral","positive","negative"]
    data=pd.read_csv(src)
    columns=data.columns
    columns=columns[1:len(columns)]
    result=pd.DataFrame(data=0,columns=polarities,index=columns)
    max_sentence_length=0
    max_aspects_nums=0
    for i in range(len(data)):
        row= data.iloc[i,:]
        sentenc_len=len(row.iloc[0])
        max_sentence_length=max(sentenc_len,max_sentence_length)
        aspect_nums=0
        for j in range(1,len(row)):
            if row.iloc[j] is not None and not pd.isna(row.iloc[j]):
                index=columns[j-1]
                column=polarities[int(row.iloc[j])]
                result.loc[index,column]=result.loc[index,column]+1
                aspect_nums=aspect_nums+1
        max_aspects_nums=max(aspect_nums,max_aspects_nums)
    result.to_excel(target)
    print(max_sentence_length)
    print(max_aspects_nums)
# 320 5 300 4
def complex_distribution(src:str,label:str,target:str):
    columns=["<50","50~100","100~150","150~200","200~250","250~300",">300"]
    indexs=[1,2,3,4,5]
    match_count=np.zeros((5,7))
    total_count=np.zeros((5,7))
    src_data=pd.read_csv(src)
    label_data=pd.read_csv(label)
    for i in range(len(src_data)):
        row_src=src_data.iloc[i,:]
        row_label=label_data.iloc[i,:]
        column=int(len(row_src.iloc[0])/50)
        matchs=0
        aspect_nums=0
        for j in range(1,len(row_src)):
            if row_src.iloc[j] is not None and not pd.isna(row_src.iloc[j]):
                aspect_nums=aspect_nums+1
                if row_src.iloc[j]==row_label.iloc[j]:
                    matchs=matchs+1
        match_count[aspect_nums-1][column]=match_count[aspect_nums-1][column]+matchs
        total_count[aspect_nums-1][column]=total_count[aspect_nums-1][column]+aspect_nums
    result=pd.DataFrame(data=0,index=indexs,columns=columns)
    for i in range(5):
        for j in range(7):
            if total_count[i][j]>0:
                result.loc[indexs[i],columns[j]]=total_count[i][j]
    result.to_excel(target)
def heatMap(src_list:list,label:str,target:str,props:list):
    columns=["<50","50~100","100~150","150~200","200~250","250~300",">300"]
    indexs=[1,2,3,4,5]
    match_count=np.zeros((5,7))
    total_count=np.zeros((5,7))
    label_data=pd.read_csv(label)
    for src in src_list:
        src_data=pd.read_csv(src)
        for i in range(len(src_data)):
            row_src=src_data.iloc[i,:]
            row_label=label_data.iloc[i,:]
            column=int(len(row_src.iloc[0])/50)
            matchs=0
            aspect_nums=0
            for j in range(1,len(row_src)):
                if row_src.iloc[j] is not None and not pd.isna(row_src.iloc[j]):
                    aspect_nums=aspect_nums+1
                    if row_src.iloc[j]==row_label.iloc[j]:
                        matchs=matchs+1
            match_count[aspect_nums-1][column]=match_count[aspect_nums-1][column]+matchs
            total_count[aspect_nums-1][column]=total_count[aspect_nums-1][column]+aspect_nums
    result=pd.DataFrame(data=0,index=indexs,columns=columns)
    for i in range(5):
        for j in range(7):
            if total_count[i][j]==0:
                continue
            if total_count[i][j]>10:
                result.loc[indexs[i],columns[j]]=float(match_count[i][j])/float(total_count[i][j])/(sum(props)/len(src_list))
            else:
                result.loc[indexs[i],columns[j]]=0
    result.to_excel(target)
def drawOneHeatMap(src:str,title:str):

    figure=plt.figure(dpi=160)
    df=pd.read_excel(src,index_col=0)
    plt.title(title,y=-0.2)
    seaborn.heatmap(data=df,  cmap=plt.get_cmap('Reds'),annot=True,
                    mask=df <=0
                )
    plt.tick_params(labelsize=8)
    plt.xticks(rotation=40)
    plt.subplots_adjust(wspace=0, hspace=0,bottom=0.15,)
    return figure
def drawHeatMap(src:list,target:str,title:list):
    pp = PdfPages(target)
    for i in range(len(src)):
        figure=drawOneHeatMap(src[i],title[i])
        pp.savefig(figure)
    pp.close()
if __name__=="__main__":
    src=["D:/pythonWork/ACSA_Prompt/data/statistics/mams_simple_heatMap_mean.xlsx",
         "D:/pythonWork/ACSA_Prompt/data/statistics/mams_heatMap_mean.xlsx",
         "D:/pythonWork/ACSA_Prompt/data/statistics/14_simple_heatMap_mean.xlsx",
         "D:/pythonWork/ACSA_Prompt/data/statistics/14_heatMap_mean.xlsx"]
    target="D:/pythonWork/ACSA_Prompt/data/statistics/heatMap.pdf"
    title=["(a) mams with SPG-FSACSA ","(b) mams with PG-FSACSA","(c) rest14 with SPG-FSACSA","(d) rest14 with PG-FSACSA"]
    drawHeatMap(src,target,title)
    '''
    src_list=["D:/pythonWork/ACSA_Prompt/data/result_data/mams_simple_five-shot_6259.csv",
              "D:/pythonWork/ACSA_Prompt/data/result_data/mams_simple_one-shot_6115.csv",
              "D:/pythonWork/ACSA_Prompt/data/result_data/mams_simple_zero-shot_6115.csv"]
    props=[0.6259,0.6115,0.6115]
    #props=[1,1,1]
    label="D:/pythonWork/ACSA_Prompt/data/processed_data/mams_test.csv"
    target="D:/pythonWork/ACSA_Prompt/data/statistics/mams_simple_heatMap_mean.xlsx"
    heatMap(src_list,label,target,props)
    '''