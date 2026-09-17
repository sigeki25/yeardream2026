from transformers import AutoTokenizer, AutoModelForSequenceClassification

# 1. 로컬에서 학습을 마친 모델과 토크나이저 로드
model_id = 'distilbert-base-uncased'
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSequenceClassification.from_pretrained(model_id)

# 2. hugging face 에 PUSH
# 토큰의 권한이 write 여야 한다.
repo_id = 'jihookuku/test_upload_model'
print('model 과 토크나이저 업로드 중...')
tokenizer.push_to_hub(repo_id)
model.push_to_hub(repo_id)
print('Upload complete!!!!')