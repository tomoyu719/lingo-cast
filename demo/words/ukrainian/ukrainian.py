import json
import os

ukrainian_strs = 'АаБбВвГгҐґДдЕеЄєЖжЗзИиІіЇїЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЬьЮюЯя'
_str = ' -—\''
path = '/Users/kitanotoshiyuki/lingo-cast/demo/outputs/ukrainian/'
file_names = os.listdir(path)
strs = set()
for n in file_names:
    with open(path + n) as f:
        df = json.load(f)
    for d in df:
        for sent in d['examples_with_prob_sum'].keys():
            for s in sent:
                if s not in ukrainian_strs + _str:
                    print(sent)
                    

print(strs)
        