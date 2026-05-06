# data_mining_final_project
# 🔬 Semiconductor Cycle Prediction

> **DRAM 시장 사이클 국면 분류 및 전환 시점 예측**
>
> *Semiconductor Cycle Prediction Using Data Mining Techniques*

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Northumbria University · Data Mining (ITM) · Final Project · 2026

---

## 📌 Project Overview

본 프로젝트는 과거 DRAM 가격 데이터와 거시경제 지표를 결합하여 반도체 시장의 **사이클 국면(업/다운/횡보)을 자동 분류**하고, **다음 사이클 전환 시점을 예측**하는 데이터 마이닝 프로젝트입니다.

### Objectives

- DRAM 가격 변화율 기반 업사이클 / 다운사이클 / 횡보 국면 자동 분류
- PCA를 통한 거시 변수 차원 축소 및 핵심 주성분 추출
- Decision Tree · kNN 모델 성능 비교를 통한 최적 분류기 선택
- 2027년 하반기 다운사이클 전환 가능성 데이터 기반 분석

---

## 🏗️ Analysis Pipeline

```
[Raw Data] → [Preprocessing] → [PCA] → [Modeling] → [Evaluation]
                  │                │          │
                  │                │          ├── Decision Tree Classifier
                  │                │          ├── Regression Tree (파생 피처)
                  │                │          └── kNN (비교 모델)
                  │                │
                  │                └── Scree Plot → 주성분 개수 결정
                  │
                  ├── StandardScaler (표준화)
                  ├── Lag Feature 생성 (t-1, t-2, t-4)
                  └── k-means 군집화 (레이블 타당성 검증)
```

| Step | Method | Week | Role |
|------|--------|------|------|
| Step 0 | StandardScaler | W12 | PCA 전처리 — 단위 차이 제거 |
| Step 1 | PCA + Scree Plot | W12 | 차원 축소 및 핵심 주성분 추출 |
| Step 1-EDA | k-means + Silhouette Score | W11 | 3-class 레이블 타당성 검증 |
| Step 2 | Regression Tree | W09 | 다음 분기 DRAM 가격 수치 예측 |
| Step 3 | Decision Tree Classifier | W09 | 업/다운/횡보 국면 최종 분류 |
| Baseline | kNN | W10 | DT와 성능 비교 — 모델 선택 근거 |

---

## 📊 Data Sources

| Data | Source | Method |
|------|--------|--------|
| DRAM 분기별 평균 가격 | TrendForce / Statista | 수동 수집 |
| 반도체 출하량 · 시장 규모 | WSTS | 월별 공개 데이터 |
| 기업 Capex · 재고 | 삼성전자 · SK하이닉스 (DART) | 분기 실적 공시 |
| 금리 · PMI 등 거시 지표 | FRED | `fredapi` 자동 수집 |

### Target Label Definition

DRAM 가격의 전분기 대비 변화율(QoQ%)을 기준으로 3개 클래스로 분류합니다.

| Class | Condition | Interpretation |
|-------|-----------|----------------|
| Upcycle | QoQ > +5% | 가격 상승 — 수요 > 공급 |
| Sideways | -5% ≤ QoQ ≤ +5% | 가격 안정 — 수급 균형 |
| Downcycle | QoQ < -5% | 가격 하락 — 공급 > 수요 |

---

## 🛠️ Tech Stack

- **Language**: Python 3.9+
- **ML Framework**: scikit-learn
- **Data Collection**: `fredapi`, `pandas`
- **Visualization**: `matplotlib`, `seaborn`
- **Environment**: Google Colab / Jupyter Notebook

---

## 📁 Project Structure

```
data_mining_final_project/
├── README.md
├── data/
│   ├── raw/                  # 원본 데이터 (DRAM 가격, FRED, DART)
│   └── processed/            # 전처리 완료 데이터
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_eda_clustering.ipynb
│   ├── 03_pca_analysis.ipynb
│   ├── 04_modeling.ipynb
│   └── 05_evaluation.ipynb
├── src/
│   ├── data_loader.py        # 데이터 수집 유틸리티
│   ├── preprocessing.py      # 전처리 및 피처 엔지니어링
│   └── models.py             # 모델 학습 및 평가
├── docs/
│   └── slides/               # 발표 슬라이드
├── requirements.txt
└── LICENSE
```

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install -r requirements.txt
```

### Quick Start

```python
# 1. FRED 데이터 수집
from src.data_loader import fetch_fred_data
macro_data = fetch_fred_data(start="1990-01-01")

# 2. 전처리 및 피처 생성
from src.preprocessing import create_features
features = create_features(dram_prices, macro_data, lags=[1, 2, 4])

# 3. 모델 학습 및 평가
from src.models import train_and_evaluate
results = train_and_evaluate(features, target="cycle_label")
```

---

## 📈 Evaluation Metrics

| Metric | Description |
|--------|-------------|
| Confusion Matrix (3×3) | 클래스별 정분류 / 오분류 현황 |
| F1-Score (Macro) | 클래스 불균형 대응 |
| Stratified 5-fold CV | 클래스 비율 유지 교차 검증 |
| Feature Importance | 주성분별 분류 기여도 |
| Baseline Comparison | 다수 클래스 예측 대비 성능 |

---

## 👥 Team

| Member | Role | Details |
|--------|------|---------|
| 팀원 1 | 데이터 수집 · 전처리 | WSTS, FRED, DART 수집 / Lag 피처 / StandardScaler |
| 팀원 2 | 모델 구현 | PCA → k-means → Regression Tree → DT → kNN |
| 팀원 3 | 시각화 · 발표 | Scree Plot, 트리 시각화, Confusion Matrix, 슬라이드 |

---

## 📅 Timeline

| Milestone | Date | Deliverable |
|-----------|------|-------------|
| 1차 발표 | 2026.05.07 | 기획 초안 — 문제 정의, 데이터 계획, 방법론 |
| 2차 발표 | TBD | 중간 결과 — 데이터 수집 완료, 모델 실험 비교 |
| 최종 발표 | TBD | 최종 결론 — 모델 확정, 사이클 전환 예측, 한계 분석 |

---

## 📚 References

- Lecture Notes: Data Mining ITM Week 09–12 (Northumbria University)
- [WSTS — World Semiconductor Trade Statistics](https://www.wsts.org)
- [FRED — Federal Reserve Economic Data](https://fred.stlouisfed.org)
- [TrendForce DRAM Price Report](https://www.trendforce.com)
- [DART 전자공시시스템](https://dart.fss.or.kr)

---

## 📄 License

This project is for academic purposes as part of the Data Mining (ITM) course at Northumbria University.
