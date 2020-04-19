# RentHouseEvaluatorApp

 SUUMOから物件情報を取得し、回帰で家賃予想を行うアプリ
 
 実行順序は以下の通り
 
 1. SUUMOから物件情報をスクレイピングと前処理 
    1. get_bukken_data.py
        - インプット ： モデルを構築したい路線のSUUMOのURL
        - アウトプット： 物件情報のCSVファイル
    2. preprocess.py
        - インプット ： ⅰで作成した物件情報のCSVファイル
        - アウトプット： 前処理を行ったCSV
 
 2. 特徴量選択とモデル作成
    1. select_features.py
        - インプット ： 1の結果CSVファイル
        - アウトプット： 不要な特徴量を削除した物件情報CSVファイル
    2. regression.py
        ランダムフォレスト回帰で家賃予想を行う
        ※2年間のランニングコストを予想する
 
 3. modelをFLASKで使用する
 ```
 $export FLASK_APP=webapp
 
 $export FLASK_ENV=development
 
 $flask run
 ```
