import airflow
import pendulum
import uuid

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator,BranchPythonOperator
from airflow.exceptions import AirflowException
from airflow.decorators import task
from sklearn.metrics import accuracy_score, f1_score
import torch.optim as optim
import torch
from kobert_transformers import get_tokenizer
import json

def _set_congig(**context):
    print(" config 설정 :디렉토리 및 파일 이름")
    with open('/tmp/config_dir.json') as f:
        config = json.load(f)
    if config['device'] == "cuda":
        print(config['device'])
        config['device'] = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    elif config['device'] == "cpu":
        config['device'] = torch.device('cpu')

def _set_tokenizer_config(**context):
    print("토크나이저 컽피그 세팅으로 파일 저장..")
    tokenizer = get_tokenizer()
    vocab = tokenizer.token2idx
    tokenizer_config = dict()
    tokenizer_config['pad_id'] = vocab['[PAD]']
    tokenizer_config['cls_id'] = vocdb['[CLS]']
    tokenizer_config['sep_id'] = vocab['[SEP]']
    tokenizer_config['unk_id'] = vocab['[UNK]']

    with open("/tmp/tokenizer_config.json","w", encoding='utf-8') as make_file:
        json.dump(tokenizer_config, make_file, indent="\t")

def _select_dataset(**context):
    with open('/tmp/config_dir.json') as f:
        config = json.load(f)
    if config['new_data'] == "true":
        return "load_new_data"
    else:
        return "load_old_data"

def _load_old_data(**context):
    print("old dataset(train+test) load (OLD)...")

def _load_new_data(**context):
    print("new dataset(train+test) load (NEW)...")

def _join_dataset(**context):
    print("join all dataset")
    print("test랑 트레인 따로 모아야,,,")

def _check_dataset(**context):
    print("Check all dataset label")

def _sampling_dataset(**context):
    print("sampling all dataset ")


def _set_model_param(**context):
    print("setting model param of config")

def _train_model(**context):
    print("train model")

def _evaluate_model(**context):
    print("evaluate model")
    print("validation dataset 결과를 디비에 저장해야함")

def _select_model(**context):
    print("select model")
    print("여기서 데이터셋이랑 학습 정확도 결과 봐야함,,,")

def _select_ckpt(**context):
    print("checkpoint 선택해서 학습..")

def _deploy_model(**context):
    print("model 배포하기...")

train_dag= DAG(
    dag_id = "train_dag",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval= None,
)
inference_dag = DAG(
    dag_id = "inference_dag",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval= None,
)


set_configuration = PythonOperator(
    task_id="set_config", python_callable= _set_congig, dag= train_dag
)

set_tokenizer_config= PythonOperator(
    task_id="set_tokenizer_config", python_callable= _set_tokenizer_config, dag= train_dag
)

select_dataset = BranchPythonOperator(
    task_id="select_dataset", python_callable= _select_dataset, dag= train_dag
)

load_old_data = PythonOperator(
    task_id="load_old_data", python_callable=_load_old_data, dag= train_dag
)

load_new_data = PythonOperator(
    task_id="load_new_data", python_callable=_load_new_data, dag= train_dag
)

join_dataset_dummy = DummyOperator(task_id="join_dummy", trigger_rule="none_failed", dag= train_dag)

join_dataset = PythonOperator(
    task_id="join_dataset", python_callable=_join_dataset, dag= train_dag
)

set_model_param = PythonOperator(
    task_id ="set_model_param", python_callable=_set_model_param, dag= train_dag
)

train_model = PythonOperator(
    task_id="train_model", python_callable=_train_model, dag= train_dag
)

select_checkpoint = PythonOperator(
    task_id="select_ckpt", python_callable=_select_ckpt, dag= train_dag
)

evaluate_model = PythonOperator(
    task_id="evaluate_model", python_callable=_evaluate_model, dag= train_dag
)
deploy_model = PythonOperator(
    task_id="deploy_model", python_callable=_deploy_model, dag= train_dag
)
select_model= PythonOperator(
    task_id="select_model", python_callable=_select_model, dag= train_dag
)

set_configuration >> set_tokenizer_config >> select_dataset >> [load_old_data, load_new_data] >> join_dataset_dummy >> join_dataset >> set_model_param >> train_model >> evaluate_model >> deploy_model

select_checkpoint >> train_model
select_model >> deploy_model

# train_model = PythonOperator(
#     task_id="train_model", python_callable=_train_model)
# deploy_model = PythonOperator(
#     task_id="deploy_model",
#     python_callable=_deploy_model,
#     templates_dict={
#         "model_id":"{{task_instance.xcom_pull()}}"
#     }
# )

# latest_only = PythonOperator(task_id="latest_only",python_callable=_latest_only)