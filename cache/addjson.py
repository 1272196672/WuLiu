import os
from os.path import join as pjoin
import json

name_emb = {"东方明珠塔": [
    1.509062,
    2.044332
  ]}


output_dir = 'D:\Download_Code\Anaconda\Lib\site-packages\pyecharts\datasets'

listdir = os.listdir(output_dir)
if 'city_coordinates.json' in listdir:
    fr = open(pjoin(output_dir, 'city_coordinates.json'), encoding='utf-8')
    model = json.load(fr)
    fr.close()

    for i in name_emb:
        model[i] = name_emb[i]

    jsObj = json.dumps(model)

    with open(pjoin(output_dir, 'city_coordinates.json'), "w", encoding='utf-8') as fw:
        fw.write(jsObj)
        fw.close()