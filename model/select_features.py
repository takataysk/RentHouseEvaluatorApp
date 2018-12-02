import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

### データを可視化し、特徴選択を行う ###
#データのロード
data = pd.read_csv('./csv/preprocess_bukken_kobeline.csv', sep=',', encoding='utf-16')

#駅毎の物件数
plt.figure()
vc = data['最寄駅'].value_counts().plot(kind="bar")
plt.tight_layout()
plt.show()
plt.close('all')

#駅毎の費用の分布
data['費用（万）'] = data['費用'] / 10000
sns.boxplot(x='最寄駅', y="費用（万）", data=data)
sns.despine(offset=10, trim=True)
plt.xticks(rotation=45)
#plt.ylim([0,300])
plt.tight_layout()
plt.show()
plt.close('all')

#徒歩30分以上は徒歩とは言えないので削除
df = pd.read_csv('./csv/input_bukken_kobeline.csv', sep=',', encoding='utf-16')
df.drop(['Unnamed: 0'], axis=1, inplace=True)
df = df[(df['駅徒歩'] <= 31)]

#駅徒歩と費用の散布図
plt.scatter(df['駅徒歩'], df['費用'] / 10000)
plt.ylabel('費用（万）')
plt.xlabel('駅徒歩')
plt.show()

#特徴量間の相関を確認
r = np.corrcoef(df.values.T)
hm = sns.heatmap(r,
                cbar=True,
                annot=True,
                square=False,
                cmap="Blues",
                fmt='.2f',
                annot_kws={'size': 5},
                yticklabels=df.columns.values,
                xticklabels=df.columns.values)
plt.tight_layout()
plt.show()

#多重共線性を排除するため、占有面積と間取りKと建物高さを削除
df.drop(['専有面積'], axis=1, inplace=True)
df.drop(['間取りK'], axis=1, inplace=True)
df.drop(['建物高さ'], axis=1, inplace=True)

#特徴選択結果をcsvで保存
df.to_csv('./csv/feat_select_bukken_kobeline.csv', sep=',', encoding='utf-16')