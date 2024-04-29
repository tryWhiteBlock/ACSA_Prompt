from predict import  do_predict

if __name__ =="__main__":
    train_src = "./data/processed_data/mams_train.csv"
    prompt_file = "./prompts1.txt"
    test_src = "./data/processed_data/mams_test.csv"
    result_file = "./data/result_data/mams_zero-shot.csv"
    shot_nums = 0
    do_predict(train_src,prompt_file,test_src,result_file,shot_nums,True)