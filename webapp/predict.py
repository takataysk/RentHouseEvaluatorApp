import functools
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
import numpy as np
import pandas as pd
import pickle
import os

os.chdir(os.path.dirname(__file__))
os.chdir('../')

with open('model/regressor/randomforest_model.pickle', 'rb') as f:
    model = pickle.load(f)

bp = Blueprint('predict', __name__)    # Blueprintの実装

@bp.route('/')
def index():
    return render_template('/index.html')

@bp.route('/predict', methods=('GET', 'POST'))
def predict():
    if request.method == 'POST':
        ekitoho = int(request.form['ekitoho'])
        madori = request.form['madori'].upper()
        madori_dk = 0
        madori_l = 0
        madori_s = 0

        if 'DK' in madori:
            madori_dk = 1
        madori = madori.replace('DK','')       
        madori = madori.replace('K','')
        madori = madori.replace('R','')

        if 'L' in madori:
            madori_l = 1        
        madori = madori.replace('L','')

        if 'S' in madori:
            madori_s = 1        
        madori = madori.replace('S','')
        madori = int(madori)

        moyori = request.form['moyori']
        umeda = 0
        juso = 0
        kanzakigawa = 0
        sonoda = 0
        tsukaguchi = 0
        mukonoso = 0
        nishikita = 0
        shukugawa = 0
        ashiyagawa = 0
        okamoto = 0
        mikage = 0
        rokko = 0
        ojikoen = 0
        kasuganomichi = 0
        kobe = 0
        
        if moyori == "umeda":
            umeda = 1
        elif moyori == "juso":
            juso = 1
        elif moyori == "kanzakigawa":
            kanzakigawa = 1
        elif moyori == "sonoda":
            sonoda = 1
        elif moyori == "tsukaguchi":
            tsukaguchi = 1
        elif moyori == "mukonoso":
            mukonoso = 1
        elif moyori == "nishikita":
            nishikita = 1
        elif moyori == "shukugawa":
            shukugawa = 1
        elif moyori == "ashiyagawa":
            ashiyagawa = 1
        elif moyori == "okamoto":
            okamoto = 1
        elif moyori == "mikage":
            mikage = 1
        elif moyori == "rokko":
            rokko = 1
        elif moyori == "ojikoen":
            ojikoen = 1
        elif moyori == "kasuganomichi":
            kasuganomichi = 1
        elif moyori == "kobe":
            kobe = 1
        
        chikunen = int(request.form['chikunen'])
        kai = int(request.form['kai'])

        if (request.form['yachin'] == "") or (request.form['kanrihi'] == "") \
                or (request.form['shikikin'] == "") or (request.form['reikin'] ==""):
            hiyou = "不明"
            print(hiyou)
        else:
            yachin = int(request.form['yachin'])
            kanrihi = int(request.form['kanrihi'])
            shikikin = int(request.form['shikikin'])
            reikin = int(request.form['reikin'])
            hiyou = (yachin + kanrihi) * 24 + shikikin + reikin

        input = [[ekitoho, madori, madori_dk, madori_l, madori_s, chikunen, kai, rokko, juso, sonoda, tsukaguchi, shukugawa, okamoto, mikage, kasuganomichi, umeda, mukonoso, ojikoen, kanzakigawa, kobe, ashiyagawa, nishikita]]

        post = {}
        post['predict'] = int(model.predict(input))
        post['answer'] = hiyou
        
        return render_template('predict.html', post=post)

