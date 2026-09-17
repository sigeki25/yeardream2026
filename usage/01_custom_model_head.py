"""
    사전학습모델은 본체(backbone)와 헤드(Head)로 구분된다.
    Backbone - 문장을 이해하고 임배딩하는 부분을 담당
    Head - 받은 임베딩 내용을 우리가 원하는 최종 결과로 바꿔주는 부분
"""
import torch
from torch import nn, no_grad
from transformers import PreTrainedModel, PreTrainedConfig, AutoModel, AutoTokenizer, AutoConfig


# 1단계 : 커스텀 모델 만들기
class CustomClassifier(PreTrainedModel):

    def __init__(self, config: PreTrainedConfig):  # 생성자(클래스가 객체화될 때 가장먼저 실행)
        super().__init__(config)  # 부모 초기화를 위해 전달
        # (1) backbone 생성
        # config 는 config.json(모델 설계도)
        self.backbone = AutoModel.from_config(config)

        # backbone 이 출력하는 백터 차월 알아내기
        hidden_size = config.hidden_size  # 768 차원

        # (2) 커스텀 헤드 만들기 - 받아온 백터들을 원하는 결과로 추출
        # 영화 리뷰를 가지고 긍정/부정 등을 구분하는 것을 할 예정
        self.custom_head = nn.Sequential(
            nn.Linear(hidden_size, hidden_size // 2),  # 768 -> 384
            nn.ReLU(),  # 활성함수
            nn.Dropout(0.3),  # 30% 무작위 끄기(전교 1등 재우기), 과적합 방지
            nn.Linear(hidden_size // 2, 2)  # 384 -> 2
        )

        self.post_init()  # 가중치 초기화

    # model() 을 실행하면 forward() 가 실행 된다.
    def forward(self, input_ids, attention_mask=None):
        # 1. backbone 에 입력을 넣어서 결과를 받는다.
        outputs = self.backbone(input_ids=input_ids, attention_mask=attention_mask)
        print(f"outputs shape : {outputs.last_hidden_state.shape}")  # [문장 수, 토큰 수, 백터 수]
        # [CLS] - 시작 토큰 (해당 문장에 대표되는 내용을 담고 있다.)
        cls_vec = outputs.last_hidden_state[:, 0, :]
        print(f"[CLS] vector : {cls_vec}")
        # 2. 커스텀헤드에 보내서 최종 결과값을 받아낸다.
        return self.custom_head(cls_vec)


# 2단계 : 토크나이저와 모델
model_id = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_id)
# 해당 모델의 셀계도를 불러옴
config = AutoConfig.from_pretrained(model_id)
model = CustomClassifier(config)  # 해당 설계도 전달

# 3단계 : 동작 확인
sentences = [
    "I really loved this movie, it was fantastic!",
    "This was a waste of time, I hated it."
]

inputs = tokenizer(sentences, padding=True, truncation=True, max_length=128, return_tensors="pt")
print(inputs)
# 검증모드로 변경
model.eval()  # 학습 과정은 필요없이 추론 경과만 보고자 할 때

with no_grad():
    logit = model(inputs["input_ids"], inputs["attention_mask"])

print(f"model 출력 {logit}")
""" 부정 긍정
[ 0.2213, -0.1968],
[ 0.2626, -0.1953]
"""
# dim=1|-1 : 가로방향으로 연산, dim=0 : 세로방향으로 연산
prob = torch.softmax(logit, dim=-1)
print(prob)

pred = torch.argmax(prob, dim=-1)
print(f"예측 결과(0:NAV/1:POS) : {pred}")

# 모델 저장
save_path = "./my_custom_model"
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)