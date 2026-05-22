import pandas as pd
df = pd.read_csv('dataset.csv')
df_0500 = df[df['VDS_CD'].str.startswith('0500')]
print(len(df_0500))
print(df_0500.head())
# 지점 목록 확인
print(df_0500['VDS_CD'].unique())
print(f"지점 수: {df_0500['VDS_CD'].nunique()}")

# 결측치 비율
print(f"결측치 비율: {(df_0500['SPD_AVG']==-1).sum()/len(df_0500)*100:.1f}%")

# 속도 기본 통계
valid = df_0500[df_0500['SPD_AVG'] != -1]
print(f"평균속도 평균: {valid['SPD_AVG'].mean():.1f}")
print(f"평균속도 표준편차: {valid['SPD_AVG'].std():.1f}")
df_0500['센서타입'] = df_0500['VDS_CD'].str[4:7]
print(df_0500['센서타입'].value_counts())

# 이정 기준으로 구간 나누기
df_0500['이정'] = df_0500['VDS_CD'].str[7:12].astype(int)

print(df_0500['이정'].min())  # 시작점
print(df_0500['이정'].max())  # 끝점
print(df_0500['이정'].describe())

# 구간 컬럼 추가
def get_group(ieong):
    if ieong <= 6000:  return '그룹1_도심'
    if ieong <= 13000: return '그룹2_산악'
    return '그룹3_해안'

df_0500['구간'] = df_0500['이정'].apply(get_group)

# 구간별 지점 수 확인
print(df_0500.groupby('구간')['VDS_CD'].nunique())

# 구간별 평균속도
valid = df_0500[df_0500['SPD_AVG'] != -1]
print(valid.groupby('구간')['SPD_AVG'].mean())
print(valid.groupby('구간')['SPD_AVG'].mean().round(1))
print(valid.groupby('구간')['SPD_AVG'].std().round(1))

valid = df_0500[df_0500['SPD_AVG'] != -1]

print(f"원활(>80):    {(valid['SPD_AVG']>80).sum()/len(valid)*100:.1f}%")
print(f"서행(40~80):  {((valid['SPD_AVG']>=40)&(valid['SPD_AVG']<=80)).sum()/len(valid)*100:.1f}%")
print(f"정체(<40):    {(valid['SPD_AVG']<40).sum()/len(valid)*100:.1f}%")