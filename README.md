# BookApp


## Develop Environment Setup
- Install conda. Follow instructions [here](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).
- Create conda environment:
```commandline
conda create --name book-chat python=3.9
conda activate book-chat
pip install -r requirements.txt
```
## Run Backend
```commandline
cd BookChat
fastapi dev main.py
```


