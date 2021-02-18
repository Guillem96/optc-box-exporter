import os
import sys
import json
import shutil
import requests
import functools
from pathlib import Path
import multiprocessing as mp
from typing import Optional, Tuple

import click
import tqdm.auto as tqdm

from optcbx.units import viable_unit


def get_portrait_url(cid: Optional[str]) -> str:
    if cid is None:
        return 'https://onepiece-treasurecruise.com/wp-content/themes/onepiece-treasurecruise/images/noimage.png'
    elif cid == '0742': 
        return 'https://onepiece-treasurecruise.com/wp-content/uploads/f0742-2.png'
    elif cid ==  '3000': 
        return 'https://onepiece-treasurecruise.com/wp-content/uploads/f3000_1.png'
    elif cid == '2262': 
        return 'http://onepiece-treasurecruise.com/en/wp-content/uploads/sites/2/f5011.png'
    elif cid == '2263': 
        return 'http://onepiece-treasurecruise.com/en/wp-content/uploads/sites/2/f5012.png'
    elif cid == '2500': 
        return 'http://onepiece-treasurecruise.com/en/wp-content/uploads/sites/2/f2500.png'
    elif cid ==  '3333': 
        return 'http://onepiece-treasurecruise.com/en/wp-content/uploads/sites/2/f5013.png'
    elif cid ==  '3334': 
        return 'http://onepiece-treasurecruise.com/en/wp-content/uploads/sites/2/f5014.png'
    elif cid == '2399':
        return 'http://onepiece-treasurecruise.com/en/wp-content/uploads/sites/2/f5015.png'
    elif cid == '2784': 
        return '../res/character_10642_t1.png'
    elif cid ==  '3339': 
        return '../res/character_10852_t1.png'
    elif cid ==  '3340': 
        return '../res/character_10853_t1.png'
    elif cid == '2663': 
        return '../res/character_10713_t1.png'
    elif cid == '2664': 
        return '../res/character_10714_t1.png'
    elif cid == '2685':
        return 'http://onepiece-treasurecruise.com/en/wp-content/uploads/sites/2/f5025.png'
    elif cid == '2686':
        return 'http://onepiece-treasurecruise.com/en/wp-content/uploads/sites/2/f5026.png'
    elif cid ==  '3347': 
        return '../res/character_1508_t1.png'
    elif cid ==  '3348': 
        return '../res/character_1509_t1.png'
    elif cid ==  '3349': 
        return '../res/character_1510_t1.png'
    elif cid ==  '3350': 
        return '../res/character_1511_t1.png'
    elif cid ==  '3351': 
        return '../res/character_10861_t1.png'
    elif cid ==  '3352': 
        return '../res/character_10862_t1.png'
    elif cid ==  '3353': 
        return '../res/character_10994_t1.png'
    elif cid ==  '3354': 
        return '../res/character_10995_t1.png'
    elif cid == '2772':
        return 'https://onepiece-treasurecruise.com/en/wp-content/uploads/sites/2/f5037.png'
    elif cid ==  '3356': 
        return '../res/character_10869_t1.png'
    elif cid ==  '3357': 
        return '../res/character_10870_t1.png'
    elif cid ==  '3358': 
        return '../res/character_10867_t1.png'
    elif cid ==  '3359': 
        return '../res/character_10868_t1.png'
    elif cid ==  '3360': 
        return '../res/character_11037_t1.png'
    elif cid ==  '3361': 
        return '../res/character_11038_t1.png'
    elif cid ==  '2768': 
        return '../res/character_10258_t1.png'
    elif cid ==  '2769': 
        return '../res/character_10259_t1.png'
    elif cid ==  '2770': 
        return '../res/character_10262_t1.png'
    elif cid ==  '2771': 
        return '../res/character_10263_t1.png'
    elif cid ==  '3366': 
        return '../res/character_10858_t1.png'
    elif cid ==  '3367': 
        return '../res/character_10859_t1.png'
    elif cid ==  '3368': 
        return '../res/character_10860_t1.png'
    elif cid == '2919':
        return '../res/character_10891_t1.png'
    elif cid ==  '3370': 
        return 'http://onepiece-treasurecruise.com/en/wp-content/uploads/sites/2/f5052.png'
    elif cid ==  '3371': 
        return '../res/character_11243_t.png'
    elif cid ==  '3372': 
        return '../res/character_11244_t.png'
    elif cid ==  '3373': 
        return '../res/character_11245_t.png'
    elif cid ==  '3374': 
        return 'http://onepiece-treasurecruise.com/en/wp-content/uploads/sites/2/f5053.png'
    elif cid ==  '3375': 
        return '../res/character_10863_t.png'
    elif cid ==  '3376': 
        return '../res/character_10864_t.png'
    elif cid == '2929':
        return '../res/character_11221_t1.png'
    elif cid == '2930':
        return '../res/character_11199_t1.png'
    elif cid ==  '3380': 
        return '../res/character_11333_t1.png'
    elif cid ==  '3381': 
        return '../res/KDugejE.png'
    elif cid ==  '3382': 
        return '../res/character_11615_t1.png'
    elif cid ==  '3383': 
        return '../res/character_11760_t.png'
    elif cid ==  '3384': 
        return '../res/character_11400_t1.png'
    elif cid ==  '3385': 
        return '../res/character_11338_t1.png'
    elif cid == '2909':
        return '../res/character_11173_t1.png'
    elif cid == '3370':
        return '../res/character_10891_t1.png'
    elif cid == '2440':
        return '../res/character_10643_t1.png'
    elif cid == '2441':
        return '../res/character_10644_t1.png'
    elif cid ==  '5000': 
        return '../res/character_10185_t1.png'
    elif cid ==  '5001': 
        return '../res/character_10186_t1.png'
    elif cid ==  '5002': 
        return '../res/character_10187_t1_int.png'
    elif cid ==  '5003': 
        return '../res/character_10187_t1_psy.png'
    elif cid ==  '5004': 
        return '../res/character_10173_t1.png'
    elif cid ==  '5005': 
        return '../res/character_10174_t1.png'
    elif cid ==  '5006': 
        return '../res/character_10177_t1_qck.png'
    elif cid ==  '5007': 
        return '../res/character_10177_t1_str.png'
    elif cid ==  '5008': 
        return '../res/character_10175_t1.png'
    elif cid ==  '5009': 
        return '../res/character_10176_t1.png'
    elif cid ==  '5010': 
        return '../res/character_10178_t1_qck.png'
    elif cid ==  '5011': 
        return '../res/character_10178_t1_str.png'
    elif cid ==  '5012': 
        return '../res/character_10181_t1.png'
    elif cid ==  '5013': 
        return '../res/character_10182_t1.png'
    elif cid ==  '5014': 
        return '../res/character_10183_t1_psy.png'
    elif cid ==  '5015': 
        return '../res/character_10183_t1_dex.png'
    elif cid ==  '5016': 
        return '../res/character_10344_t1.png'
    elif cid ==  '5017': 
        return '../res/character_10345_t1.png'
    elif cid ==  '5018': 
        return '../res/character_10348_t1_psy.png'
    elif cid ==  '5019': 
        return '../res/character_10348_t1_int.png'
    elif cid ==  '5020': 
        return '../res/character_10346_t1.png'
    elif cid ==  '5021': 
        return '../res/character_10347_t1.png'
    elif cid ==  '5022': 
        return '../res/character_10349_t1_psy.png'
    elif cid ==  '5023': 
        return '../res/character_10349_t1_int.png'
    elif cid ==  '5024': 
        return '../res/character_10496_t1.png'
    elif cid ==  '5025': 
        return '../res/character_10497_t1.png'
    elif cid ==  '5026': 
        return '../res/character_10498_t1_dex.png'
    elif cid ==  '5027': 
        return '../res/character_10498_t1_str.png'
    elif cid ==  '5028': 
        return '../res/character_10636_t1.png'
    elif cid ==  '5029': 
        return '../res/character_10637_t1.png'
    elif cid ==  '5030': 
        return '../res/character_10640_t1_int.png'
    elif cid ==  '5031': 
        return '../res/character_10640_t1_dex.png'
    elif cid ==  '5032': 
        return '../res/character_10638_t1.png'
    elif cid ==  '5033': 
        return '../res/character_10639_t1.png'
    elif cid ==  '5034': 
        return '../res/character_10641_t1_int.png'
    elif cid ==  '5035': 
        return '../res/character_10641_t1_dex.png'
    elif cid ==  '5036': 
        return '../res/character_10649_t1.png'
    elif cid ==  '5037': 
        return '../res/character_10650_t1.png'
    elif cid ==  '5038': 
        return '../res/character_10653_t1_dex.png'
    elif cid ==  '5039': 
        return '../res/character_10653_t1_qck.png'
    elif cid ==  '5040': 
        return '../res/character_10651_t1.png'
    elif cid ==  '5041': 
        return '../res/character_10652_t1.png'
    elif cid ==  '5042': 
        return '../res/character_10654_t1_dex.png'
    elif cid ==  '5043': 
        return '../res/character_10654_t1_qck.png'
    elif cid == '2818':
        return '../res/character_10707_t1.png'
    elif cid == '2819':
        return '../res/character_10708_t1.png'
    elif cid ==  '5044': 
        return '../res/character_10703_t.png'
    elif cid ==  '5045': 
        return '../res/character_10704_t.png'
    elif cid ==  '5046': 
        return '../res/character_10707_t1_qck.png'
    elif cid ==  '5047': 
        return '../res/character_10707_t1_int.png'
    elif cid ==  '5048': 
        return '../res/character_10705_t.png'
    elif cid ==  '5049': 
        return '../res/character_10706_t.png'
    elif cid ==  '5050': 
        return '../res/character_10708_t1_qck.png'
    elif cid ==  '5051': 
        return '../res/character_10708_t1_int.png'
    elif cid ==  '5052': 
        return '../res/character_10720_t1.png'
    elif cid ==  '5053': 
        return '../res/character_10721_t1.png'
    elif cid ==  '5054': 
        return '../res/character_10724_t1_psy.png'
    elif cid ==  '5055': 
        return '../res/character_10722_t1.png'
    elif cid ==  '5056': 
        return '../res/character_10723_t1.png'
    elif cid ==  '5057': 
        return '../res/character_10725_t1_psy.png'
    elif cid ==  '5058': 
        return '../res/character_10735_t1.png'
    elif cid ==  '5059': 
        return '../res/character_10736_t1.png'
    elif cid ==  '5060': 
        return '../res/character_10739_t1_psy.png'
    elif cid ==  '5061': 
        return '../res/character_10739_t1_qck.png'
    elif cid ==  '5062': 
        return '../res/character_10737_t1.png'
    elif cid ==  '5063': 
        return '../res/character_10738_t1.png'
    elif cid ==  '5064': 
        return '../res/character_10740_t1_psy.png'
    elif cid ==  '5065': 
        return '../res/character_10740_t1_qck.png'
    elif cid ==  '5066': 
        return '../res/character_10832_t1.png'
    elif cid ==  '5067': 
        return '../res/character_10833_t1.png'
    elif cid ==  '5068': 
        return '../res/character_10836_t1_int.png'
    elif cid ==  '5069': 
        return '../res/character_10836_t1_qck.png'
    elif cid ==  '5070': 
        return '../res/character_10834_t1.png'
    elif cid ==  '5071': 
        return '../res/character_10835_t1.png'
    elif cid ==  '5072': 
        return '../res/character_10837_t1_int.png'
    elif cid ==  '5073': 
        return '../res/character_10837_t1_qck.png'
    elif cid ==  '5074': 
        return '../res/character_10950_t1.png'
    elif cid ==  '5075': 
        return '../res/character_10951_t1.png'
    elif cid ==  '5076': 
        return '../res/character_10952_t1_dex.png'
    elif cid ==  '5077': 
        return '../res/character_10952_t1_qck.png'
    elif cid ==  '5078': 
        return '../res/character_10773_t1.png'
    elif cid ==  '5079': 
        return '../res/character_10774_t1.png'
    elif cid ==  '5080': 
        return '../res/character_10775_t1_int.png'
    elif cid ==  '5081': 
        return '../res/character_10775_t1_qck.png'
    elif cid ==  '5082': 
        return '../res/character_10784_t1.png'
    elif cid ==  '5083': 
        return '../res/character_10785_t1.png'
    elif cid ==  '5084': 
        return '../res/character_10788_t1_dex.png'
    elif cid ==  '5085': 
        return '../res/character_10788_t1_qck.png'
    elif cid ==  '5086': 
        return '../res/character_10786_t1.png'
    elif cid ==  '5087': 
        return '../res/character_10787_t1.png'
    elif cid ==  '5088': 
        return '../res/character_10789_t1_dex.png'
    elif cid ==  '5089': 
        return '../res/character_10789_t1_qck.png'
    elif cid ==  '5090': 
        return '../res/character_10816_t1.png'
    elif cid ==  '5091': 
        return '../res/character_10817_t1.png'
    elif cid ==  '5092': 
        return '../res/character_10820_t1_int.png'
    elif cid ==  '5093': 
        return '../res/character_10818_t1.png'
    elif cid ==  '5094': 
        return '../res/character_10819_t1.png'
    elif cid ==  '5095': 
        return '../res/character_10821_t1_int.png'
    elif cid ==  '5096': 
        return '../res/character_10871_t1.png'
    elif cid ==  '5097': 
        return '../res/character_10872_t1.png'
    elif cid ==  '5098': 
        return '../res/character_10875_t1_str.png'
    elif cid ==  '5099': 
        return '../res/character_10875_t1_dex.png'
    elif cid ==  '5100': 
        return '../res/character_10873_t1.png'
    elif cid ==  '5101': 
        return '../res/character_10874_t1.png'
    elif cid ==  '5102': 
        return '../res/character_10876_t1_str.png'
    elif cid ==  '5103': 
        return '../res/character_10876_t1_dex.png'
    elif cid ==  '5104': 
        return '../res/character_10877_t1.png'
    elif cid ==  '5105': 
        return '../res/character_10878_t1.png'
    elif cid ==  '5106': 
        return '../res/character_10881_t1_psy.png'
    elif cid ==  '5107': 
        return '../res/character_10881_t1_str.png'
    elif cid ==  '5108': 
        return '../res/character_10879_t1.png'
    elif cid ==  '5109': 
        return '../res/character_10880_t1.png'
    elif cid ==  '5110': 
        return '../res/character_10882_t1_psy.png'
    elif cid ==  '5111': 
        return '../res/character_10882_t1_str.png'
    elif cid ==  '5112': 
        return '../res/character_10883_t1.png'
    elif cid ==  '5113': 
        return '../res/character_10884_t1.png'
    elif cid ==  '5114': 
        return '../res/character_10887_t1_qck.png'
    elif cid ==  '5115': 
        return '../res/character_10887_t1_psy.png'
    elif cid ==  '5116': 
        return '../res/character_10885_t1.png'
    elif cid ==  '5117': 
        return '../res/character_10886_t1.png'
    elif cid ==  '5118': 
        return '../res/character_10888_t1_qck.png'
    elif cid ==  '5119': 
        return '../res/character_10888_t1_psy.png'
    elif cid ==  '5120': 
        return '../res/character_10826_t1.png'
    elif cid ==  '5121': 
        return '../res/character_10827_t1.png'
    elif cid ==  '5122': 
        return '../res/character_10830_t1_dex.png'
    elif cid ==  '5123': 
        return '../res/character_10830_t1_int.png'
    elif cid ==  '5124': 
        return '../res/character_10828_t1.png'
    elif cid ==  '5125': 
        return '../res/character_10829_t1.png'
    elif cid ==  '5126': 
        return '../res/character_10831_t1_dex.png'
    elif cid ==  '5127': 
        return '../res/character_10831_t1_int.png'
    elif cid ==  '5128': 
        return '../res/character_10778_t1.png'
    elif cid ==  '5129': 
        return '../res/character_10779_t1.png'
    elif cid ==  '5130': 
        return '../res/character_10782_t1_str.png'
    elif cid ==  '5131': 
        return '../res/character_10782_t1_dex.png'
    elif cid ==  '5132': 
        return '../res/character_10780_t1.png'
    elif cid ==  '5133': 
        return '../res/character_10781_t1.png'
    elif cid ==  '5134': 
        return '../res/character_10783_t1_str.png'
    elif cid ==  '5135': 
        return '../res/character_10783_t1_dex.png'
    elif cid ==  '5136': 
        return '../res/character_10895_t1.png'
    elif cid ==  '5137': 
        return '../res/character_10896_t1.png'
    elif cid ==  '5138': 
        return '../res/character_10899_t1_int.png'
    elif cid ==  '5139': 
        return '../res/character_10899_t1_dex.png'
    elif cid ==  '5140': 
        return '../res/character_10897_t1.png'
    elif cid ==  '5141': 
        return '../res/character_10898_t1.png'
    elif cid ==  '5142': 
        return '../res/character_10900_t1_int.png'
    elif cid ==  '5143': 
        return '../res/character_10900_t1_dex.png'
    elif cid ==  '5144': 
        return '../res/character_10910_t1.png'
    elif cid ==  '5145': 
        return '../res/character_10911_t1.png'
    elif cid ==  '5146': 
        return '../res/character_10914_t1_str.png'
    elif cid ==  '5147': 
        return '../res/character_10914_t1_int.png'
    elif cid ==  '5148': 
        return '../res/character_10912_t1.png'
    elif cid ==  '5149': 
        return '../res/character_10913_t1.png'
    elif cid ==  '5150': 
        return '../res/character_10915_t1_str.png'
    elif cid ==  '5151': 
        return '../res/character_10915_t1_int.png'
    elif cid ==  '5152': 
        return '../res/character_10916_t1.png'
    elif cid ==  '5153': 
        return '../res/character_10917_t1.png'
    elif cid ==  '5154': 
        return '../res/character_10920_t1_str.png'
    elif cid ==  '5155': 
        return '../res/character_10920_t1_psy.png'
    elif cid ==  '5156': 
        return '../res/character_10918_t1.png'
    elif cid ==  '5157': 
        return '../res/character_10919_t1.png'
    elif cid ==  '5158': 
        return '../res/character_10921_t1_str.png'
    elif cid ==  '5159': 
        return '../res/character_10921_t1_psy.png'
    elif cid ==  '5160': 
        return '../res/character_10954_t1.png'
    elif cid ==  '5161': 
        return '../res/character_10955_t1.png'
    elif cid ==  '5162': 
        return '../res/character_10958_t1_dex.png'
    elif cid ==  '5163': 
        return '../res/character_10958_t1_str.png'
    elif cid ==  '5164': 
        return '../res/character_10956_t1.png'
    elif cid ==  '5165': 
        return '../res/character_10957_t1.png'
    elif cid ==  '5166': 
        return '../res/character_10959_t1_dex.png'
    elif cid ==  '5167': 
        return '../res/character_10959_t1_str.png'
    elif cid ==  '5168': 
        return '../res/character_10960_t1.png'
    elif cid ==  '5169': 
        return '../res/character_10961_t1.png'
    elif cid ==  '5170': 
        return '../res/character_10964_t1_int.png'
    elif cid ==  '5171': 
        return '../res/character_10964_t1_psy.png'
    elif cid ==  '5172': 
        return '../res/character_10962_t1.png'
    elif cid ==  '5173': 
        return '../res/character_10963_t1.png'
    elif cid ==  '5174': 
        return '../res/character_10965_t1_int.png'
    elif cid ==  '5175': 
        return '../res/character_10965_t1_psy.png'
    elif cid ==  '5176': 
        return '../res/character_10803_t1.png'
    elif cid ==  '5177': 
        return '../res/character_10804_t1.png'
    elif cid ==  '5178': 
        return '../res/character_10805_t1_str.png'
    elif cid ==  '5179': 
        return '../res/character_10805_t1_int.png'
    elif cid ==  '5180': 
        return '../res/character_10889_t1.png'
    elif cid ==  '5181': 
        return '../res/character_10890_t1.png'
    elif cid ==  '5182': 
        return '../res/character_10891_t1_dex.png'
    elif cid ==  '5183': 
        return '../res/character_10891_t1_qck.png'
    elif cid ==  '5184': 
        return '../res/character_11099_t1.png'
    elif cid ==  '5185': 
        return '../res/character_11100_t1.png'
    elif cid ==  '5186': 
        return '../res/character_11102_t1_qck.png'
    elif cid ==  '5187': 
        return '../res/character_11166_t1.png'
    elif cid ==  '5188': 
        return '../res/character_11167_t1.png'
    elif cid ==  '5189': 
        return '../res/character_11168_t1_psy.png'
    elif cid ==  '5190': 
        return '../res/character_11168_t1_int.png'
    elif cid ==  '5191': 
        return '../res/character_11187_t1.png'
    elif cid ==  '5192': 
        return '../res/character_11188_t1.png'
    elif cid ==  '5193': 
        return '../res/character_11191_t1_str.png'
    elif cid ==  '5194': 
        return '../res/character_11191_t1_dex.png'
    elif cid ==  '5195': 
        return '../res/character_11189_t1.png'
    elif cid ==  '5196': 
        return '../res/character_11190_t1.png'
    elif cid ==  '5197': 
        return '../res/character_11192_t1_str.png'
    elif cid ==  '5198': 
        return '../res/character_11192_t1_dex.png'
    elif cid ==  '5199': 
        return '../res/character_11129_t1.png'
    elif cid ==  '5200': 
        return '../res/character_11130_t1.png'
    elif cid ==  '5201': 
        return '../res/character_11131_t1_str.png'
    elif cid ==  '5202': 
        return '../res/character_11227_t1.png'
    elif cid ==  '5203': 
        return '../res/character_11228_t1.png'
    elif cid ==  '5204': 
        return '../res/character_11231_t1_dex.png'
    elif cid ==  '5205': 
        return '../res/character_11231_t1_int.png'
    elif cid ==  '5206': 
        return '../res/character_11229_t1.png'
    elif cid ==  '5207': 
        return '../res/character_11230_t1.png'
    elif cid ==  '5208': 
        return '../res/character_11232_t1_dex.png'
    elif cid ==  '5209': 
        return '../res/character_11232_t1_int.png'
    elif cid ==  '5210': 
        return '../res/character_11260_t1.png'
    elif cid ==  '5211': 
        return '../res/character_11261_t1.png'
    elif cid ==  '5212': 
        return '../res/character_11262_t1_dex.png'
    elif cid ==  '5213': 
        return '../res/character_11262_t1_int.png'
    elif cid ==  '5214': 
        return '../res/character_11254_t1.png'
    elif cid ==  '5215': 
        return '../res/character_11255_t1.png'
    elif cid ==  '5216': 
        return '../res/character_11258_t1_str.png'
    elif cid ==  '5217': 
        return '../res/character_11256_t1.png'
    elif cid ==  '5218': 
        return '../res/character_11257_t1.png'
    elif cid ==  '5219': 
        return '../res/character_11259_t1_str.png'
    elif cid ==  '5220': 
        return '../res/character_11306_t1.png'
    elif cid ==  '5221': 
        return '../res/character_11307_t1.png'
    elif cid ==  '5222': 
        return '../res/character_11310_t1_psy.png'
    elif cid ==  '5223': 
        return '../res/character_11310_t1_qck.png'
    elif cid ==  '5224': 
        return '../res/character_11308_t1.png'
    elif cid ==  '5225': 
        return '../res/character_11309_t1.png'
    elif cid ==  '5226': 
        return '../res/character_11311_t1_psy.png'
    elif cid ==  '5227': 
        return '../res/character_11311_t1_qck.png'
    elif cid ==  '5228': 
        return '../res/character_11318_t1.png'
    elif cid ==  '5229': 
        return '../res/character_11319_t1.png'
    elif cid ==  '5230': 
        return '../res/character_11322_t1_str.png'
    elif cid ==  '5231': 
        return '../res/character_11322_t1_qck.png'
    elif cid ==  '5232': 
        return '../res/character_11320_t1.png'
    elif cid ==  '5233': 
        return '../res/character_11321_t1.png'
    elif cid ==  '5234': 
        return '../res/character_11323_t1_str.png'
    elif cid ==  '5235': 
        return '../res/character_11323_t1_qck.png'
    elif cid ==  '5236': 
        return '../res/character_11324_t1.png'
    elif cid ==  '5237': 
        return '../res/character_11325_t1.png'
    elif cid ==  '5238': 
        return '../res/character_11328_t1_qck.png'
    elif cid ==  '5239': 
        return '../res/character_11328_t1_dex.png'
    elif cid ==  '5240': 
        return '../res/character_11326_t1.png'
    elif cid ==  '5241': 
        return '../res/character_11327_t1.png'
    elif cid ==  '5242': 
        return '../res/character_11329_t1_qck.png'
    elif cid ==  '5243': 
        return '../res/character_11329_t1_dex.png'
    elif cid ==  '5244': 
        return '../res/character_11314_t1.png'
    elif cid ==  '5245': 
        return '../res/character_11315_t1.png'
    elif cid ==  '5246': 
        return '../res/character_11317_t1_int.png'
    elif cid ==  '5247': 
        return '../res/character_11371_t1.png'
    elif cid ==  '5248': 
        return '../res/character_11372_t1.png'
    elif cid ==  '5249': 
        return '../res/character_11375_t1_str.png'
    elif cid ==  '5250': 
        return '../res/character_11375_t1_psy.png'
    elif cid ==  '5251': 
        return '../res/character_11373_t1.png'
    elif cid ==  '5252': 
        return '../res/character_11374_t1.png'
    elif cid ==  '5253': 
        return '../res/character_11376_t1_str.png'
    elif cid ==  '5254': 
        return '../res/character_11376_t1_psy.png'
    elif cid ==  '5255': 
        return '../res/smuAu7N.png'
    elif cid ==  '5256': 
        return '../res/ZPSk7PQ.png'
    elif cid ==  '5257': 
        return '../res/KDugejE_qck.png'
    elif cid ==  '5258': 
        return '../res/KDugejE_int.png'
    elif cid ==  '5259': 
        return '../res/character_11532_t1.png'
    elif cid ==  '5260': 
        return '../res/character_11533_t1.png'
    elif cid ==  '5261': 
        return '../res/character_11534_t1_psy.png'
    elif cid ==  '5262': 
        return '../res/character_11534_t1_int.png'
    elif cid ==  '5263': 
        return '../res/character_11661_t1.png'
    elif cid ==  '5264': 
        return '../res/character_11660_t1.png'
    elif cid ==  '5265': 
        return '../res/character_11662_t1_dex.png'
    elif cid ==  '5266': 
        return '../res/character_11662_t1_psy.png'
    elif cid ==  '5267': 
        return '../res/character_11582_t1.png'
    elif cid ==  '5268': 
        return '../res/character_11583_t1.png'
    elif cid ==  '5269': 
        return '../res/character_11586_t1_str.png'
    elif cid ==  '5270': 
        return '../res/character_11586_t1_psy.png'
    elif cid ==  '5271': 
        return '../res/character_11584_t1.png'
    elif cid ==  '5272': 
        return '../res/character_11585_t1.png'
    elif cid ==  '5273': 
        return '../res/character_11587_t1_str.png'
    elif cid ==  '5274': 
        return '../res/character_11587_t1_psy.png'

    else:
        return 'https://onepiece-treasurecruise.com/wp-content/uploads/f' + cid + '.png';


def generate_id(idx: int) -> str:
    idx = str(idx)
    padding = 4 - len(idx)
    return '0' * padding + idx


def download_portrait(p: Tuple[str, str], out_path: Path):
    cid, url = p
    dst_path = str(out_path / f"{cid}.png")

    if url.startswith('../res'):
        url = url.replace('../res', 'https://optc-db.github.io/res')

    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(dst_path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    else:
        print("Error while downloading:", url)


@click.command()
@click.option('--units', type=click.Path(file_okay=True, exists=True), 
              default='data/units.json')
@click.option('--output', type=click.Path(file_okay=False), 
              default='data/Portrait')
def main(units: str, output: str):
    """Download all characters portraits
    """
    output = Path(output)
    output.mkdir(exist_ok=True, parents=True)

    units = json.load(open(units))
    units = [viable_unit(o) for o in units]
    portraits_urls = [(i, get_portrait_url(generate_id(i))) 
                      for i, u in enumerate(units, start=1) if u]

    download_fn = functools.partial(download_portrait, out_path=output)
    p = mp.Pool(mp.cpu_count())
    try:
        r = list(tqdm.tqdm(p.imap(download_fn, portraits_urls), 
                           total=len(portraits_urls)))
        p.close()
    except Exception as e:
        print(str(e))
    except KeyboardInterrupt:
        print ("You cancelled the program!")
        p.terminate()
        p.join()
        sys.exit(1)


if __name__ == "__main__":
    main()

