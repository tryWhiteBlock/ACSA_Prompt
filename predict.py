import pandas as pd
import json
import re
import time
import threading
import os
from prompts import gen_system,guide,answer,simple_guide

def gen_prompts(shot_nums:int,src:str,prompt_file:str):
    data=pd.read_csv(src)
    data=data.sample(frac=1)
    columns=data.columns
    sentences=[]
    aspects=[]
    answers=[]
    for i in range(shot_nums):
        row=data.loc[i,:]
        sentence=row.iloc[0]
        aspect_categories=[]
        answer=[]
        for j in range(1,len(row)):
            if row.iloc[j] is not None and not pd.isna(row.iloc[j]):
                aspect_categories.append(columns[j])
                answer.append(row.iloc[j])
        answers.append(answer)
        aspects.append(aspect_categories)
        sentences.append(sentence)
    history=gen_system(sentences,aspects,answers)
    prompts=json.dumps(history)
    with open(prompt_file,'w') as f:
        f.write(prompts)

def predict(sentence:str,aspects:list,prompt_file:str,length):
    if length<=0:
        return []
    with open(prompt_file,'r') as f:
        prompt=f.read();
    prompt=json.loads(prompt)
    prompt=guide(prompt,aspects,sentence)
    pattern=r'\[[012, ]*\]'
    matches=[]
    while True:
        result=answer(prompt)
        result=result.replace("\\","")
        matches=re.findall(pattern,result)
        if len(matches)>0:
            for j in range(len(matches)):
                result=json.loads(matches[j])
                if len(result)==length:
                    return result
                else:
                    print("length not match")
                    print(len(result)-length)
        time.sleep(5)
def simple_predict(sentence:str,aspects:list,prompt_file:str,length):
    if length<=0:
        return []
    with open(prompt_file,'r') as f:
        prompt=f.read();
    prompt=json.loads(prompt)
    prompt=simple_guide(prompt,aspects,sentence)
    pattern=r'\[[012, ]*\]'
    matches=[]
    while True:
        result=answer(prompt)
        result=result.replace("\\","")
        matches=re.findall(pattern,result)
        if len(matches)>0:
            for j in range(len(matches)):
                result=json.loads(matches[j])
                if len(result)==length:
                    return result
                else:
                    print("length not match")
                    print(len(result)-length)
        time.sleep(5)
def comput_accuracy(test_src,result_src):
    data=pd.read_csv(test_src)
    result_data=pd.read_csv(result_src)
    current_match=0.0
    total_labels=0.0
    for i in range(len(data)):
        row=result_data.loc[i,:]
        for j in range(1,len(row)):
                if row.iloc[j] is not None and not pd.isna(row.iloc[j]):
                    if data.loc[i,:].iloc[j]==row.iloc[j]:
                        current_match=current_match+1
                    total_labels=total_labels+1
    print(current_match/total_labels)
def do_predict(train_src,prompt_file,test_src,result_file,shot_nums,simple):
    gen_prompts(shot_nums,train_src,prompt_file)
    data=pd.read_csv(test_src)
    columns=data.columns
    result_data=[]
    to_continue=True
    current_match=0.0
    total_labels=0.0
    round=0
    if to_continue and os.path.isfile(result_file):
        result_dataFrame=pd.read_csv(result_file)
        columns1=result_dataFrame.columns
        for i in range(len(result_dataFrame)):
            dit={}
            row=result_dataFrame.loc[i,:]
            sentence=row.iloc[0]
            dit["sentence"]=sentence
            for j in range(1,len(row)):
                if row.iloc[j] is not None and not pd.isna(row.iloc[j]):
                    dit[columns1[j]]=row.iloc[j]
                    if data.loc[i,:].iloc[j]==row.iloc[j]:
                        current_match=current_match+1
                    total_labels=total_labels+1
            result_data.append(dit)
    for i in range(len(result_data),len(data)):
        dit={}
        row=data.loc[i,:]
        sentence=row.iloc[0]
        dit["sentence"]=sentence
        aspects=[]
        labels=[]
        for j in range(1,len(row)):
            if row.iloc[j] is not None and not pd.isna(row.iloc[j]):
                aspects.append(columns[j])
                labels.append(row.iloc[j])
        if simple:
            result=simple_predict(sentence,aspects,prompt_file,len(aspects))
        else:
            result=predict(sentence,aspects,prompt_file,len(aspects))
        print(result)
        print(labels)
        for j in range(len(aspects)):
            dit[aspects[j]]=result[j]
            if result[j]== labels[j]:
                current_match=current_match+1
        total_labels=total_labels+len(aspects)
        result_data.append(dit)
        round=round+1
        if round==50:
            round=0
            result_dataFrame=pd.DataFrame(result_data)
            result_dataFrame.to_csv(result_file,index=False)
        print(i)
        print("current accuracy:%f"%(current_match/total_labels))
    result_dataFrame=pd.DataFrame(result_data)
    result_dataFrame.to_csv(result_file,index=False)
    comput_accuracy(test_src,result_file)
if __name__ =="__main__":
    train_src1="./data/processed_data/mams_train.csv"
    prompt_file1="./prompts1.txt"
    test_src1="./data/processed_data/mams_test.csv"
    result_file1="./data/result_data/mams_zero-shot.csv"
    shot_nums1=0
    thread1=threading.Thread(target=do_predict, args=(train_src1, prompt_file1,test_src1,result_file1,shot_nums1,False))
    train_src2="./data/processed_data/mams_train.csv"
    prompt_file2="./prompts2.txt"
    test_src2="./data/processed_data/mams_test.csv"
    result_file2="./data/result_data/mams_one-shot.csv"
    shot_nums2=1
    thread2=threading.Thread(target=do_predict, args=(train_src2, prompt_file2,test_src2,result_file2,shot_nums2,False))
    train_src3="./data/processed_data/mams_train.csv"
    prompt_file3="./prompts3.txt"
    test_src3="./data/processed_data/mams_test.csv"
    result_file3="./data/result_data/mams_five-shot.csv"
    shot_nums3=5
    thread3=threading.Thread(target=do_predict, args=(train_src3, prompt_file3,test_src3,result_file3,shot_nums3,False))
    #thread1.start()
    #thread2.start()
    #thread3.start()
    comput_accuracy(test_src3,result_file3)
    while threading.active_count() >1:
        print(threading.active_count())
        time.sleep(10)
