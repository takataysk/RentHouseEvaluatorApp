import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import pickle

def lenear_regression():
    df = pd.read_csv('./csv/feat_select_bukken_kobeline.csv', sep = ',',encoding='utf-16')

    #不要な列を削除
    df.drop(['Unnamed: 0'], axis=1, inplace=True)

    #分析後出力される変数
    coef = np.zeros((22,1))
    intercept = np.zeros(1)
    score = np.zeros(1)

    #root mean square error（RMSE）
    rmse = np.zeros(1)

    #8割を学習、2割をテストに使用
    dfTrain = df[0:int(len(df.index) * 0.8)]
    dfTest = df[int(len(df.index) * 0.8):len(df.index)]

    #モデルの定義
    clf = linear_model.LinearRegression()
    
    # 説明変数
    X_train = dfTrain.drop(['費用'], axis=1)
    X_train = X_train.apply(lambda x: (x - np.mean(x)) / np.std(x))
    X_train = X_train.as_matrix()
    
    # 目的変数
    Y_train = dfTrain['費用'].as_matrix()
    
    # 予測モデルを作成
    clf.fit(X_train, Y_train)

    # 回帰係数
    coef[:,0] = clf.coef_
    coef_ = pd.Series(coef[:,0])
    index = pd.Series(dfTrain.drop(['費用'], axis=1).columns.values)
    df_coef = pd.concat([index, coef_], axis=1)
    df_coef.to_csv('./csv/coef_.csv', sep=',', encoding='utf-16')

    # 切片 (誤差)
    intercept[0] = clf.intercept_
    
    # 決定係数
    score[0] = clf.score(X_train, Y_train)

    #テストの説明変数
    X_test = dfTest.drop(['費用'], axis=1)
    X_test = X_test.apply(lambda x: (x - np.mean(x)) / np.std(x))
    X_test = X_test.as_matrix()
    
    #テストの正解
    Y_test = dfTest['費用'].as_matrix()

    #テストの予測結果
    result = clf.predict(X_test)

    #RMSE計算
    rmse[0] = np.sqrt(np.mean(np.square(np.array(result - Y_test))))

    #結果可視化
    idx = np.argsort(np.array(Y_test))
    plt.plot(np.arange(0,len(Y_test)),np.array(Y_test)[idx], color='blue')
    plt.plot(np.arange(0,len(result)),np.array(result)[idx], alpha=0.4)
    plt.savefig("./img/正規化＿予測＆正解.png")
    plt.show()

    with open('./regressor/linear_model.pickle', 'wb') as f:
        pickle.dump(clf, f)

    return rmse

def random_forest_regression():
    df = pd.read_csv('./csv/feat_select_bukken_kobeline.csv', sep = ',',encoding='utf-16')

    #不要な列を削除
    df.drop(['Unnamed: 0'], axis=1, inplace=True)

    #グリッドサーチするパラメーター
    parameters = {
        'n_estimators'      : [5, 10, 30, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
        'max_features'      : ['auto'],
        'random_state'      : [0],
        'min_samples_split' : [2, 3, 5, 10],
        'max_depth'         : [None, 3, 5, 10]
    }

    #root mean square error（RMSE）
    rmse = np.zeros(1)

    #8割を学習、2割をテストに使用    
    dfTrain = df[0:int(len(df.index) * 0.8)]
    dfTest = df[int(len(df.index) * 0.8):len(df.index)]

    #モデルの定義
    clf = GridSearchCV(RandomForestRegressor(), parameters, verbose=1, n_jobs = -1)
    
    # 説明変数
    X_train = dfTrain.drop(['費用'], axis=1)
    X_train = X_train.as_matrix()
    
    # 目的変数
    Y_train = dfTrain['費用'].as_matrix()
    
    # 予測モデルを作成
    clf.fit(X_train, Y_train)

    print(clf.best_estimator_)

    #テストの説明変数
    X_test = dfTest.drop(['費用'], axis=1)
    X_test = X_test.as_matrix()
    
    #テストの正解
    Y_test = dfTest['費用'].as_matrix()

    #テストの予測結果
    result = clf.predict(X_test)

    #RMSE計算
    rmse[0] = np.sqrt(np.mean(np.square(np.array(result - Y_test))))

    #結果可視化
    idx = np.argsort(np.array(Y_test))
    plt.plot(np.arange(0,len(Y_test)),np.array(Y_test)[idx], color='blue')
    plt.plot(np.arange(0,len(result)),np.array(result)[idx], alpha=0.4)
    plt.savefig("./img/randomForest_正規化＿予測＆正解.png")
    plt.show()

    with open('./regressor/randomforest_model.pickle', 'wb') as f:
        pickle.dump(clf, f)
    
    return rmse

if __name__ == "__main__":
    rmse_lenear = lenear_regression()
    rmse_randomforest = random_forest_regression()

    index = np.array([1, 2])
    label = ["linear", "RandomForest"]
    height = np.array([rmse_lenear[0], rmse_randomforest[0]])
    plt.bar(index, height, tick_label=label, align="center")
    plt.show()