curl -sfL https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh -o standalone_embed.sh
bash standalone_embed.sh start

pip install -r requirements.txt

python milvus/init.py

fastapi dev main.py