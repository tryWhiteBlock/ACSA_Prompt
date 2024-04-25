from chat import chat
import json
def gen_system(sentences:list,aspects:list,answers:list):
    dic={}
    dic["role"]="system"
    dic["content"]='''
    You need to complete a task named 'Aspect category sentiment analysis' under the user's guide.
    Aspect category sentiment analysis (ACSA) aims to identify sentiment polarities of predefined aspect categories in a sentence.'''
    minLength=min(len(sentences),len(aspects))
    minLength=min(len(answers),minLength)
    if minLength>0:
        examples=[]
        for i in range(minLength):
            example={}
            example["sentence"]=sentences[i]
            example["aspect categories"]=aspects[i]
            example["final answer"]=answers[i]
            examples.append(example)
        dic["content"]=dic["content"]+"Here are some examples with sentence, aspect categories, and final answer:\n"+json.dumps(examples)
    return [dic]

def guide(history:list,aspect:list,sentence:str):
    message=history.copy()
    guide1={}
    guide1["role"]="user"
    guide1["content"]='''
    Firstly, I will give you a list of aspect categories in a pair of square brackets, delimit by commas.You should remember and understand them.
    aspect categories:''' + str(aspect)
    message.append(guide1)
    response1={}
    response1["role"]="assistant"
    response1["content"]=chat(message)
    message.append(response1)
    guide2={}
    guide2["role"]="user"
    guide2["content"]='''
    Sencond, I will give you a sentence in a pair of single quotation marks, in which you are asked to identify sentiment polarities of predefined aspect categories later.
    To make sure you do your job better,this step, you should find out the words related to each given aspect category in the sentence.'''+"sentence:'"+sentence+"'"
    message.append(guide2)
    response2={}
    response2["role"]="assistant"
    response2["content"]=chat(message)
    message.append(response2)
    guide3={}
    guide3["role"]="user"
    guide3["content"]='''
    Now, you are supposed to identify sentiment polarities of predefined aspect categories in the given sentence.
    Be careful, before you consider a sentiment polarity of one aspect category is negative or positive, make sure you find out the reasons in the given sentence.
    Tell me the answer with the format of a list which consists of 0, 1, and 2,such as [0,1,2],0 means neutral, 1 means positive, and 2 means negative.
    The answer list should meet the following requirements:
    first, neutral should be 0, positive should be 1,and negative should be 2.
    sencond, the length of answer list should fits with the length of aspect categories list.
    third, when it comes to an indistinct sentiment polarity, consider it as neutral, tag 0.
    fourth, make the sentiment analysis as right as possible.'''
    message.append(guide3)
    return message
def simple_guide(history:list,aspect:list,sentence:str):
    message=history.copy()
    guide1={}
    guide1["role"]="user"
    guide1["content"]='''
    I will give you a list of aspect categories in a pair of square brackets,delimit by commas.Then, a sentence in a pair of single quotation marks.
    You are supposed to identify sentiment polarities of predefined aspect categories in the gived sentence.
    Be careful, before you consider a sentiment polarity of one aspect category is negative or positive, make sure you find out the reasons in the given sentence.
    Tell me the answer with the format of a list which consists of 0, 1, and 2,such as [0,1,2],0 means neutral, 1 means positive, and 2 means negative.
    The answer list should meet the following requirements:
    first, neutral should be 0, positive should be 1,and negative should be 2.
    sencond, the length of answer list should fits with the length of aspect categories list.
    third, when it comes to an indistinct sentiment polarity, consider it as neutral, tag 0.
    fourth, make the sentiment analysis as right as possible.
    aspect categories:'''+str(aspect)+"\n"+"sentence:'"+sentence+"'."
    message.append(guide1)
    return message

def answer(history):
    message=history.copy()
    response1={}
    response1["role"]="assistant"
    response1["content"]=chat(message)
    recheck={}
    recheck["role"]="user"
    recheck["content"]='''
    Say it again, neutral should be 0,positive should be 1, and negative should be 2. Inspect your answer, make sure the length and content of the final answer list is correct,
    then give me the list.
    '''
    message.append(recheck)
    answer=chat(message)
    return answer

