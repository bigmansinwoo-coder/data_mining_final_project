# 영동고속도로 교통 혼잡 예측 - 데이터 전처리 보고서

> 팀원 1 작업 결과 공유  
> Data Mining (ITM) Final Project

---

## 📌 프로젝트 개요

**연구 목적:** 영동고속도로를 도심/산악/해안 3개 구간으로 분리하여, 시간/날씨/계절 정보로 현재 교통 혼잡 국면을 분류하고, 구간별 Feature Importance 비교를 통해 정체 원인이 구간 특성에 따라 어떻게 달라지는지 분석한다.

**분석 단위:** 영동고속도로(노선번호 0500) 1시간 단위 VDS 데이터 + 기상청 ASOS 시간별 날씨 데이터

---

## 🎯 타겟 변수 (3-class 분류)

평균속도(SPD_AVG)를 기준으로 3개 클래스로 분류:

| 클래스 | 조건 | 의미 |
|---|---|---|
| `smooth` (원활) | 속도 ≥ 95 km/h | 자유 주행 |
| `slow` (서행) | 60 ≤ 속도 < 95 km/h | 교통량 증가 |
| `congested` (정체) | 속도 < 60 km/h | 실질적 정체 |

> ※ 임계값 60/95는 전체 데이터 분포(평균 92.6, 표준편차 25.1)를 고려하여 설정. 한국도로공사 공식 기준(40/80)은 데이터 분포와 맞지 않아 조정함.

---

## 📊 데이터 수집

### 1. 교통 데이터 (한국도로공사)
- **출처:** bigdata-transportation.kr
- **형식:** VDS 1시간 단위 zip 파일
- **기간:** 2023-05-19 ~ 2026-05-18 (3년치)
- **규모:** 1,080개 zip 파일 → 13,258,658행

### 2. 날씨 데이터 (기상청 ASOS)
- **출처:** 공공데이터포털 ASOS API
- **관측소:** 이천(203), 원주(114), 대관령(100)
- **기간:** 2023-05-19 ~ 2026-05-18
- **규모:** 78,912행 (관측소 × 26,304 시간)

### 3. VDS 위치 정보
- **출처:** 한국도로공사 VDS존 파일
- **용도:** VDS_CD → 실제 km 위치 매핑

---

## 🛣️ 구간 그룹핑

**원칙:** 각 기상 관측소 ±10km 범위만 사용 (전체 232km 다 쓰면 날씨 영향 희석됨)

| 구간 | 관측소 | 지점코드 | 이정 범위 |
|---|---|---|---|
| seg1_icheon (수도권) | 이천 | 203 | 72 ~ 92 km |
| seg2_wonju (내륙) | 원주 | 114 | 125 ~ 145 km |
| seg3_daegwallyeong (산악) | 대관령 | 100 | 180 ~ 200 km |

**방향:** VDE (강릉방향, 인천→강릉)만 사용 → 분석 일관성 확보

---

## 🔧 전처리 파이프라인

### Step 1: 결측치 처리 (`-1` 값)

- VDS별 -1 비율 분석 결과: 일부 센서가 100% 고장
- **임계값 30% 이상 결측인 VDS는 통째로 제외**

| 구간 | 정상 VDS / 전체 | After 행 수 |
|---|---|---|
| seg1_icheon | 15 / 24 | 319,786 |
| seg2_wonju | 17 / 19 | 431,174 |
| seg3_daegwallyeong | 19 / 20 | 477,718 |

### Step 2: 교통-날씨 병합

- **병합 키:** `SUM_YRMTHDAT` + `SUM_HR` + `segment`
- **결과:** 결측치 0건, 완벽한 병합

### Step 3: 속도 0인 행 추가 제거

- 속도 0 = 차량 없음 또는 측정 불가 → 분류에 부적합
- 의미있는 측정값만 유지

### Step 4: 파생 변수 생성

| 변수 | 설명 | 예시 |
|---|---|---|
| `hour` | 시간 (0~23) | 14 |
| `dayofweek` | 요일 (0=월 ~ 6=일) | 3 |
| `time_zone` | 시간대 구분 | morning_rush / evening_rush / midnight / normal |
| `season` | 계절 | spring / summer / fall / winter |
| `is_weekend` | 주말 여부 | 0 or 1 |
| `is_holiday` | 명절 여부 (설/추석 전후 3일) | 0 or 1 |

### Step 5: 인코딩 + 표준화

- **One-Hot Encoding:** `time_zone`, `season`
- **StandardScaler:** 수치형 변수 표준화
- **결과:** 18개 피처

---

## 📁 최종 산출물

```
data_mining_final_project/datas/seg/
├── 4_seg1_icheon_final.csv         (269,181행, 18피처 + label)
├── 4_seg2_wonju_final.csv          (427,017행, 18피처 + label)
└── 4_seg3_daegwallyeong_final.csv  (465,030행, 18피처 + label)

scaler_seg1_icheon.pkl
scaler_seg2_wonju.pkl
scaler_seg3_daegwallyeong.pkl
```

### 최종 레이블 분포

| 구간 | smooth | slow | congested |
|---|---|---|---|
| seg1_icheon | 57.3% | 36.7% | 6.0% |
| seg2_wonju | 72.5% | 26.1% | 1.4% |
| seg3_daegwallyeong | 76.3% | 23.4% | 0.3% |

> ⚠️ 클래스 불균형 존재. 모델 학습 시 `class_weight='balanced'` 또는 SMOTE 적용 권장.

---

## 🚫 Data Leakage 방지 설계

**중요 결정사항:** 현재 시점의 교통 데이터(`SPD_AVG`, `TRFFCVLM`, `OCCPNCY`)를 **피처에서 제외**

**이유:**
- 속도와 교통량은 같은 VDS 센서에서 동시 측정됨
- 속도를 타겟으로 쓰면서 교통량을 피처로 쓰면 강한 상관관계로 인해 다른 변수(날씨, 시간) 영향이 묻힘
- 결과: 모델이 "교통량 많으면 정체"만 학습 → Feature Importance 분석 무의미

**해결:** 시간/요일/계절/날씨/명절 정보만으로 분류 → "어떤 조건에서 정체가 발생하는가" 분석에 집중

---

## 📋 최종 피처 목록 (총 18개)

### 날씨 (6개, 표준화)
- `temperature` (기온, °C)
- `rainfall` (강수량, mm/h)
- `wind_speed` (풍속, m/s)
- `snow` (적설량, cm)
- `humidity` (습도, %)
- `visibility` (시정, 10m)

### 시간 (4개)
- `hour` (시간, 표준화)
- `dayofweek` (요일, 표준화)
- `is_weekend` (주말 여부, 0/1)
- `is_holiday` (명절 여부, 0/1)

### 시간대 One-Hot (4개)
- `time_zone_morning_rush`
- `time_zone_evening_rush`
- `time_zone_midnight`
- `time_zone_normal`

### 계절 One-Hot (4개)
- `season_spring`
- `season_summer`
- `season_fall`
- `season_winter`

---

## 🔜 다음 단계 (팀원 2, 3 작업)

### 팀원 2 (EDA + k-means)
- 구간별/시간대별/날씨별 정체 패턴 시각화
- k-means(k=3) 군집화 + Silhouette Score로 레이블 타당성 검증
- 명절/폭설 시즌 특이 패턴 분석

### 팀원 3 (모델링 + 평가)
- Decision Tree (베이스라인)
- Random Forest (메인 모델) - `class_weight='balanced'` 적용
- Stratified k-fold + F1-Score(macro)로 평가
- **구간별 Feature Importance 비교** ← 핵심 결과

---

## 📂 파일 구조

```
data_mining_final_project/
├── 01_clean_traffic.py       # 교통 데이터 정제
├── 02_merge_weather.py       # 교통-날씨 병합
├── 03_make_label.py          # 레이블 생성
├── 04_encoding_scale.py      # 인코딩 + 표준화
└── datas/
    ├── youngdong_all.csv     # 원본 합본 (1,326만 행)
    ├── 1_seg1_icheon_clean.csv  # 정제된 교통 데이터
    ├── 2_seg1_icheon_merged.csv # 날씨 병합 후
    ├── 3_seg1_icheon_labeled.csv # 레이블 추가
    ├── 4_seg1_icheon_final.csv  # ⭐ 최종 모델링용
    └── weather_final.csv     # 정제된 날씨 데이터
```

---

## ✅ 체크리스트

- [x] 교통 데이터 수집 (3년치, 1,080개 파일)
- [x] 영동고속도로 필터링 + 구간 그룹핑
- [x] 결측치 처리 (VDS 품질 기반)
- [x] 날씨 데이터 수집 (3개 관측소)
- [x] 교통-날씨 병합
- [x] 파생 변수 생성
- [x] 인코딩 + 표준화
- [ ] EDA (팀원 2)
- [ ] k-means 검증 (팀원 2)
- [ ] Decision Tree (팀원 3)
- [ ] Random Forest (팀원 3)
- [ ] Feature Importance 구간 비교 (팀원 3)
- [ ] 발표 슬라이드 (팀원 3)
