# 🚦 Korean Highway Traffic Congestion Prediction

> **한국 고속도로 교통 혼잡도 예측 — Data Mining Final Project**

한국도로공사 VDS(차량검지기) 교통 데이터와 기상청 ASOS 날씨 데이터를 결합하여, 고속도로 구간의 교통 혼잡 국면(원활 / 서행 / 정체)을 분류·예측하는 머신러닝 프로젝트입니다.

---

## 📌 Project Overview

| 항목 | 내용 |
|------|------|
| **주제** | 고속도로 교통 혼잡도 분류 예측 |
| **타겟 변수** | 혼잡 국면 3-class (Smooth / Slow / Congested) |
| **기준** | 평균속도 > 80 km/h → 원활, 40~80 → 서행, ≤ 40 → 정체 |
| **분류 기준 근거** | 도로교통공단 고속도로 서비스 수준(LOS) |
| **과목** | Data Mining (ITM), Northumbria University |

---

## 📊 Data Sources

### 1. 교통 데이터 — 한국도로공사 VDS
- **출처**: [공공데이터포털 (data.go.kr)](https://www.data.go.kr/)
- **내용**: 고속도로 지점별 교통량, 평균속도, 점유율 등
- **수집 주기**: 시간 단위 집계

### 2. 날씨 데이터 — 기상청 ASOS
- **출처**: [기상자료개방포털 (data.kma.go.kr)](https://data.kma.go.kr/)
- **내용**: 기온, 강수량, 적설량, 풍속, 안개 등
- **수집 주기**: 시간 단위 관측

### 3. 공휴일/명절 정보
- **출처**: 공공데이터포털
- **내용**: 법정 공휴일, 명절, 대체 휴일 여부

---

## 🔧 Methodology

### Preprocessing
- 교통 + 날씨 데이터를 날짜/시간/위치 기준으로 병합 (Join)
- 파생 변수 생성: 시간대 구분(출퇴근/심야/일반), 계절, 명절 여부, 공휴일 여부
- 수치형 변수: StandardScaler 표준화
- 범주형 변수: One-Hot Encoding
- 클래스 불균형 처리: SMOTE (Synthetic Minority Over-sampling Technique)

### Exploratory Data Analysis (EDA)
- 시간대별, 노선별, 날씨별 정체 패턴 탐색
- 클래스 분포 분석 및 시각화

### Dimensionality Reduction
- **PCA** (Principal Component Analysis): 수치형 변수 간 다중공선성 제거
- Dual-Model 접근: PCA 적용 모델 vs 미적용 모델 비교를 통해 PCA 효과 검증

### Unsupervised Validation
- **k-Means Clustering** (k=3): 비지도 학습 기반으로 데이터가 실제 3개 군집으로 분리되는지 검증
- Silhouette Score를 통한 타겟 변수 임계값(80/40 km/h) 타당성 확인

### Classification Models

| Model | Role | Description |
|-------|------|-------------|
| **Decision Tree** | Baseline | Gini Impurity 기반 분할, Cost Complexity Pruning |
| **Random Forest** | Main | Bagging 기반 앙상블, Feature Importance 분석 |
| **kNN** | Comparison | Euclidean Distance 기반 유사 사례 예측 |

### Evaluation
- **Primary Metric**: Macro F1-Score
- **Validation**: Stratified 5-Fold Cross Validation
- 3×3 Confusion Matrix 분석
- SMOTE 적용 전/후 성능 비교
- Feature Importance 비교 (날씨 vs 교통량 vs 시간대)

---

## 📁 Project Structure

```
├── data/
│   ├── raw/                  # 원시 데이터 (VDS, ASOS, 공휴일)
│   └── processed/            # 전처리 완료 데이터
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_modeling.ipynb
│   └── 05_evaluation.ipynb
├── reports/
│   ├── proposal.docx         # 프로젝트 기획서
│   └── presentation.pptx     # 발표 자료
├── README.md
└── requirements.txt
```

---

## 🛠 Tech Stack

- **Language**: Python 3.x
- **Environment**: Google Colab
- **Libraries**: pandas, numpy, scikit-learn, matplotlib, seaborn, imbalanced-learn (SMOTE)

---

## 👥 Team

Northumbria University — Data Mining (ITM) Final Project, 3인 팀

---

## 📄 License

This project is for academic purposes only.
