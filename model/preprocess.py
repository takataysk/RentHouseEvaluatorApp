import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import re
import pickle
import sys, os

df = pd.read_csv('./csv/bukken_kobeline.csv', sep=',',encoding='utf-16')
df.drop(['Unnamed: 0'], axis=1, inplace=True)

#最寄駅まで徒歩で行ける物件のみに絞る
df = df[df['駅徒歩'].str.contains('歩')]

#敷金礼金が()つきの物件はよくわからんので外す
df = df[~df['敷金'].str.contains('\(')]
df = df[~df['礼金'].str.contains('\(')]

#「-」を0に変換
df['管理費'] = df['管理費'].str.replace('-','0')
df['敷金'] = df['敷金'].str.replace('-','0')
df['礼金'] = df['礼金'].str.replace('-','0')

#平屋を1階に変換
df['建物高さ'] = df['建物高さ'].str.replace('平屋', '1階建')
df['階'] = df['階'].str.replace('平屋', '1階')

#不要な文字列の削除
df['駅徒歩'] = df['駅徒歩'].str.replace('歩', '')
df['駅徒歩'] = df['駅徒歩'].str.replace('分', '')
df['築年数'] = df['築年数'].str.replace('新築', '築0年')
df['築年数'] = df['築年数'].str.replace('築', '')
df['築年数'] = df['築年数'].str.replace('年', '')
df['建物高さ'] = df['建物高さ'].str.replace('階建', '')
df['階'] = df['階'].str.replace('階', '')
df['階'] = df['階'].str.replace('建', '')
df['管理費'] = df['管理費'].str.replace('円', '')
df['敷金'] = df['敷金'].str.replace('万円', '')
df['礼金'] = df['礼金'].str.replace('万円', '')
df['専有面積'] = df['専有面積'].str.replace('m²', '')

#文字列から数値に変換
df['賃料'] = pd.to_numeric(df['賃料'])
df['管理費'] = pd.to_numeric(df['管理費'])
df['敷金'] = pd.to_numeric(df['敷金'])
df['礼金'] = pd.to_numeric(df['礼金'])
df['築年数'] = pd.to_numeric(df['築年数'])
df['専有面積'] = pd.to_numeric(df['専有面積'])
df['駅徒歩'] = pd.to_numeric(df['駅徒歩'])

#単位を合わせるために、管理費以外を10000倍。
df['賃料'] = df['賃料'] * 10000
df['敷金'] = df['敷金'] * 10000
df['礼金'] = df['礼金'] * 10000

#2年間住むことを前提に、'賃料+管理費' * 24 + '敷/礼'を費用とする
df['費用'] = (df['賃料'] + df['管理費']) * 24 + df['敷金'] + df['礼金']

#不要なカラムを削除
df.drop(['賃料','管理費', '敷金', '礼金'], axis=1, inplace=True)

#階を数値化。地下はマイナスとして扱う
splitted = df['階'].str.split('-', expand=True)
splitted.columns = ['階1', '階2']
splitted['階1'].str.encode('cp932')
splitted['階1'] = splitted['階1'].str.replace(u'階', u'')
splitted['階1'] = splitted['階1'].str.replace(u'B', u'-')
splitted['階1'] = pd.to_numeric(splitted['階1'])
df = pd.concat([df, splitted['階1']], axis=1)
df.drop(['階'], axis=1, inplace=True)

#建物高さを数値化。地下は無視。
df['建物高さ'].str.encode('cp932')
df['建物高さ'] = df['建物高さ'].str.replace(u'地下1地上', u'')
df['建物高さ'] = df['建物高さ'].str.replace(u'地下2地上', u'')
df['建物高さ'] = df['建物高さ'].str.replace(u'地下3地上', u'')
df['建物高さ'] = df['建物高さ'].str.replace(u'地下4地上', u'')
df['建物高さ'] = df['建物高さ'].str.replace(u'地下5地上', u'')
df['建物高さ'] = df['建物高さ'].str.replace(u'地下6地上', u'')
df['建物高さ'] = df['建物高さ'].str.replace(u'地下7地上', u'')
df['建物高さ'] = df['建物高さ'].str.replace(u'地下8地上', u'')
df['建物高さ'] = df['建物高さ'].str.replace(u'地下9地上', u'')
df['建物高さ'] = df['建物高さ'].str.replace(u'階建', u'')
df['建物高さ'] = pd.to_numeric(df['建物高さ'])

#indexを振り直す
df = df.reset_index(drop=True)

#間取りを「部屋数」「DK有無」「K有無」「L有無」「S有無」に分割
df['間取りDK'] = 0
df['間取りK'] = 0
df['間取りL'] = 0
df['間取りS'] = 0
df['間取り'].str.encode('cp932')
df['間取り'] = df['間取り'].str.replace(u'ワンルーム', u'1') #ワンルームを1に変換

for x in range(len(df)):
    if 'DK' in df['間取り'][x]:
        df.loc[x,'間取りDK'] = 1
df['間取り'] = df['間取り'].str.replace(u'DK',u'')

for x in range(len(df)):
    if 'K' in df['間取り'][x]:
        df.loc[x,'間取りK'] = 1        
df['間取り'] = df['間取り'].str.replace(u'K',u'')

for x in range(len(df)):
    if 'L' in df['間取り'][x]:
        df.loc[x,'間取りL'] = 1        
df['間取り'] = df['間取り'].str.replace(u'L',u'')

for x in range(len(df)):
    if 'S' in df['間取り'][x]:
        df.loc[x,'間取りS'] = 1        
df['間取り'] = df['間取り'].str.replace(u'S',u'')
df['間取り'] = pd.to_numeric(df['間取り'])

#カラムを入れ替え
df = df[['マンション名','最寄駅', '駅徒歩','間取り','間取りDK','間取りK','間取りL','間取りS','築年数',
            '建物高さ','階1','専有面積','費用']]

#csvファイルとして保存
df.to_csv('./csv/preprocess_bukken_kobeline.csv', sep = ',',encoding='utf-16') 

#駅をダミー変数に変換
dummy_df = pd.get_dummies(df[['最寄駅']], drop_first = True)

#dfのマージ
df2 = pd.merge(df, dummy_df,left_index=True, right_index=True)

#不要なカラムの削除
df2.drop(['マンション名','最寄駅'], axis=1, inplace=True)

#テストのため順番ランダムに
df2 = df2.reindex(np.random.permutation(df2.index))

#モデルへの入力特徴量をcsvで保存
df2.to_csv('./csv/input_bukken_kobeline.csv', sep=',', encoding='utf-16')

