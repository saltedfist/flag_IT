import hashlib
import random
from base64 import encode

import config


def create_veri():
    list_num = [1,2,3,4,5,6,7,8,9,0]
    list_str = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','s','t','x','y','z']
    veri_str = random.sample(list_str,2)
    veri_num = random.sample(list_num,2)
    veri_out = random.sample(veri_num + veri_str,4)
    veri_res = str(veri_out[0]) + str(veri_out[1]) + str(veri_out[2]) + str(veri_out[3])
    return veri_res

def render_password(pw):
    m = hashlib.sha256()
    m.update(pw.encode('utf8', errors='ignore'))
    m.update(b'jfosm(3%$2";')
    m.update(config.SECRET_KEY.encode("utf8"))

    return m.hexdigest()
