# Me-RAG
This project combines **retrieval-based methods** with **large language models (LLM)** to provide accurate answers to mathematical and equation-based queries. The RAG model searches relevant context from a knowledge base and generates precise responses...

##  Installation
Make sure you have **Python 3.8** installed.  

#### install python using miniconda
1) donwload ans install miniconda from[here]("https://www.anaconda.com/docs/getting-started/miniconda/install#linux-2")
2) create a new environment using the follcwing command:
```bash
$ conda create -n rag-env python=3.8
```
3) activate the environment:
```bash
$ conda activate rag-env
```
##  Installation required packages
```bash
pip install -r requirements.txt
```
## setup the environment variables
```bash
cp .env.example .env
```
set your environment variables in the `.env` file . like `OPINAI_API_KEY`,,,,.

## run the FastApi server 
```bash
uvicorn main:app --reload --reload --host 0.0.0.0 --port 5000
```



