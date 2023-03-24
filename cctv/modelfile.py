import folium
import requests
import numpy as np
import pandas as pd
from geopy.distance import distance
from folium.plugins import HeatMap
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from haversine import haversine
from scipy.spatial.distance import cdist
from rest_framework.decorators import action
from .models import Count, Map
# 1. CSV 파일을 pandas DataFrame으로 읽기
cctv_df = pd.read_csv('dataset\cctv.csv', encoding='euc-kr')
cctv_df = cctv_df.iloc[:, :6]
cctv_df

def getlocationlist(str) :
    list_lat = []
    list_lon = []
    data = cctv_df.copy()
    
    if str == '전체' :
        for i in range(len(data)) :
            list_lat.append(data.iloc[i, 2])
            list_lon.append(data.iloc[i, 3])
            Map.objects.create(
                lat = data.iloc[i, 2],
                lon = data.iloc[i, 3],
                summary = data.iloc[i, 1],
            )
        lat = np.mean(list_lat)
        lon = np.mean(list_lon)
        return data
    else :
        new_cctv_df = data[data.loc[:, '안심 주소'].str.contains(str)]
        new_cctv_df.to_csv('cctv_{}.csv'.format(str), index=False, encoding='utf-8')
        for i in range(len(new_cctv_df)) :
            list_lat.append(new_cctv_df.iloc[i, 2])
            list_lon.append(new_cctv_df.iloc[i, 3])
            Map.objects.create(
                lat = data.iloc[i, 2],
                lon = data.iloc[i, 3],
                summary = data.iloc[i, 1],
            )
        lat = np.mean(list_lat)
        lon = np.mean(list_lon)
        return new_cctv_df
def getdong(str) :
    setcolor_df = getlocationlist(str)
    print('엔터링')
    
    # 안심cctv주소에 따라 컬러 값 지정
    setcolor_df.loc[setcolor_df.loc[:, "안심 주소"].str.contains("공사중"), "status"] = "공사"
    setcolor_df.loc[setcolor_df.loc[:, "안심 주소"].str.contains("교체예정"), "status"] = "교체예정"
    setcolor_df.loc[setcolor_df.loc[:, "안심 주소"].str.contains("철거됨"), "status"] = "철거"
    setcolor_df.loc[setcolor_df.loc[:, "status"].isnull(), "status"] = "활성"
    
    dframe = pd.DataFrame(setcolor_df["status"].value_counts())
    Count.objects.all().delete()
    for i in range(len(dframe)):
        Count.objects.create(
            status = dframe.index[i],
            counts = dframe.columns[i],
        )
def clustering(str1, str2) :
    setcolor_df = getlocationlist(str1)
    location = setcolor_df[['위도', '경도']]
    
    # KMeans 알고리즘 채택
    kmeans = KMeans(n_clusters=5, n_init=10, random_state=42)
    kmeans.fit(location)
    
    if str2 == '전체' :
        addcctv(setcolor_df, kmeans)
    else :
        Map.objects.all().delete()
        addcctv(setcolor_df, kmeans)

def addcctv(setcolor_df, kmeans) :
    # 클러스터 중 샘플 개수가 적은 3개 클러스터 선택
    cluster_df = pd.DataFrame({'cluster': kmeans.labels_})
    cluster_counts = cluster_df['cluster'].value_counts()
    cluster_indices = sorted(cluster_counts.nsmallest(3).index.tolist())
    
    for index in cluster_indices:
        cluster_samples = setcolor_df[kmeans.labels_ == index]
        cluster_centers = kmeans.cluster_centers_[index]
        center_lat = cluster_centers[0]
        center_lon = cluster_centers[1]

        # 1개에서 2개 추천
        num_samples = len(cluster_samples)
        num_recommendations = min(num_samples, 2)
        selected_samples = cluster_samples.sample(n=num_recommendations)

        # 클러스터 중심에서 가장 가까운 cctv의 위치 및 거리 찾기
        min_distance = 10000
        for _, r in selected_samples.iterrows():
            distance = haversine([center_lat, center_lon] , [r['위도'], r['경도']])
            if distance < min_distance:
                min_distance = distance
        # 거리가 충분히 멀 경우 새로운 cctv 설치를 추천
        if min_distance > 0.3:  # 예시로 0.5km 이상인 경우 추천
            Map.objects.create(
                lat = center_lat,
                lon = center_lon,
                summary = '설치 추천장소',
            )
        # 거리가 가까운 경우 적절한 거리를 두고 다시 추천
        else:
            Map.objects.create(
                lat = center_lat + 0.001,
                lon = center_lon + 0.001,
                summary = '설치 추천장소',
            )