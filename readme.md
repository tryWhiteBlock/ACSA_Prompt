# PG-FSACSA

## Introduction

This repository was used in our paper:

**Utilizing Chain-of-Thought with GPT for Enhanced Few-Shot Aspect Category Sentiment Analysis**

Please kindly give a star for this repository if you use this code.

## Requirements

python ==3.7

matplotlib==3.5.3
numpy==1.21.6
openai==1.10.0
pandas==1.3.5
seaborn==0.12.2

## Usage

`pip install -r requirements.txt`

Enter the base URL and API key for calling the GPT-3.5 API into the files api_base_url and api_key, respectively

For PG-FSACSA, call the function do_predict in predict using the parameter simple=False.

For SPG-FSACSA, call the function do_predict in predict using the parameter simple=True.

