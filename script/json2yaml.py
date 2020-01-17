#!/usr/bin/env python37
# -*- encoding: utf-8 -*-
'''
@File    :   json2yaml.py
@Time    :   2020/01/12 16:44:48
@Author  :   BenzenPenxil
@Version :   1.0
@Contact :   lunzhipenxil@gmail.com
@License :   (C)Copyright 2017-2020, Penx.Studio
@Desc    :   None
'''

# here put the import lib
import json
import yaml
import codecs
import base64
import os
import re
import tkinter
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import webbrowser

favicon_ico = "AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAAMMOAADDDgAAAAAAAAAAAAA3LBr/Py8e/0M0I/9CNSP/QzYl/0xEM/9gWEj/cGVW/3xxYP+Lfmz/kYRz/5SHdv+TiXb/k4p2/5KKd/+Rinf/k4h1/4+Ecf+LgW3/iX5r/4Z7af+CdmX/fnJf/3dpWP9uYVH/ZltJ/1dOO/9KQS//QDUj/z0wHv88Lx7/OS0a/zguHf9DMyH/QjYk/1hSQ/+CfnL/lJKG/5qVhf+XiXf/j39t/39xXP90ZlD/cWVP/3BgTP9vX0z/c2ZU/4B1Y/9+c2P/c2ZT/21fTP9oWkj/Z1lF/2ZXRf9oWkX/ZllE/2daRv9yZFH/f3Nf/4J5Zf98cmP/VEs//zowIP87Lhz/PjIf/0I1Iv90bmT/mpqR/6Cfkf+IgGz/b2FD/2VXPf9cTDf/YVI//2ZXQf9oVkD/b19R/6Gbk/+ZlIz/lJKK/5mWjv+CeGf/emtZ/25eTv9oWUb/ZFRD/2JUP/9bTTr/Vkc0/1VEMv9VRDD/YFA6/4J4X/+Jh3f/gXt1/0U9Lv9ENiL/Rjkk/2RbTv+KhXb/mZSA/5mSev+Ge13/dGlM/2xfR/9tXkj/altB/3FlU/+vqqT/vb66/6+vqf+ytbP/tra2/6Oflf+FeWb/dWVR/2VYQf9kVkD/YlQ8/19RPf9dTzr/XlM7/2peRv9+dFv/lY57/42LgP93cGX/Rzsp/0Q3JP9JOyH/Rzcf/1NEMf9nXEr/em9c/5OHcv+nnYf/r6GM/6aXff+aj3j/uLmv/8vJy/+urKT/w8a+/8nNyf/Iycr/zMrJ/6OZif+Sgmr/j4Jo/5GDbP+Wi3H/npJ8/6Wbh/+noIv/nZWD/4h/bv9uY1L/UUUy/0EyHv9BMh3/RTgl/0k8JP9PPyj/VEMx/1hJNv9cTTj/YlNA/25iUf95aln/jYNx/8vLw//T0dD/qaCW/9rVz//j5eX/3drZ/93Z2//g4uT/3tzV/6aahv+ekXj/m452/5WKcf+MgWj/g3hh/3dqV/9iVET/UkQz/009J/9KOyT/SDom/0Q2JP9KPCj/TkAr/1BCLP9XSDT/Xk88/2VXQP9pW0X/aVxI/2teR/+9t7D/09LR/5iNff+KgGf/ysS4/9XUzf/v7/D/7+/w/9jW0v/JxLn/joNu/3JkRP9yZEX/bV4//2lZOf9iUzb/YlU8/2BROv9aSjX/VUYx/05AKf9IPCX/RTck/0w+Kf9ENSP/TT4p/1xONv9gUj3/ZlhC/2tdRv9xYk7/cmNN/8zJwv/LzMT/eGhN/4ZzWv9yZEf/qaOR////////////sqya/3JhRP+Cb1b/g3BQ/39rS/97Z0j/dmJC/3BfQ/9qXUX/YFM5/1lNMv9XSjH/T0Ir/0w8Jv9IOSP/SD0m/4h+cP95cGD/TkMt/2RVPv9nWkP/bV9I/3VmTv9rXUL/tLCl/+rt6v+fk33/gW5S/4NuUv+0q5z///////////+4sqL/fmtN/4dzVf99Z03/fGpP/3pmSP93ZEP/cV9F/2lbRP9hVDn/WU0x/1ZJLv9PQir/TD0m/0g5Iv9NQiz/2dXO//b49f+CfXD/WUkx/21eQ/9uY0z/dGdO/3BjRv+ln47/9Pf3/8jCs/+FdFf/h3NU/6edi//x7/D/6uzq/6+omf+Kdlb/h3da/5aRh/+0r6z/h3pf/3ZkRv91Y0n/bmFI/2hbQf9fUjn/WUsz/1JFK/9NQCf/STsk/0o8Jv9YSjv/19LN//f39P+Jf3H/YVU9/3RoTf93bFH/d2lM/5OLd//w9PX/4+Te/49+Zv+Sgmj/zsq+//Ht7//x8vT/raWT/4l2XP+soZf/xsjI/6+qo/+Aclj/f2pP/3hmTP9xZEr/aVxF/2VXQP9dTzj/UkQs/00/Jv9JOyT/UkQt/049Jf9qXkz/7Ovn//n59v+Mg3H/dWNH/3psUP91Z0//xsCz//P39v/09vT/rKCP/9PLwf//////4+Hb//Du6//d2M7/p52S/9DOzP+0rqf/g3Vd/35sTv+DblP/e2lN/3NnTf9tX0j/aFlD/11POP9TRS//T0Eq/0s9Jv9OQCj/Vkox/05AJ/+Dd2b//////8vFu/9uWTv/fXBX/8fBuf//////9vb2//X29v/y8+///v7//+Hf2P+VhXD/19DG//37/v/W1tH/tLGj/4d3XP+Ec1X/iHdY/4NxVf98ak//eGhK/3JiR/9qWkL/XlE4/1RHL/9RQyz/Sz0n/09CKP9WSS//X1Ez/2VUN//q6OT/5eHd/3ptWP/h3dL///////n5+//9+/z/+Pr6//3////QzMH/lYZs/5h+Yf+9s6b//////8nBuP+Pe2H/kn5e/457Xf+NemH/iHVc/31pTf95Z0j/cmFE/2pZPf9iVDf/WEsx/1NFL/9OQCr/UUUq/1lNM/9jUjb/ZVI3/9TSzP/6+vj/4t7c///////6/Pz//f/9//z9/P//////29XN/5WBZf+ciGr/nIdq/6mdif/s7Oz/urWp/5mCZ/+chmv/lH9i/49+Yf+FblP/fWZG/3xuVP9zY0f/bVo8/2VWOf9ZTTL/VUcx/1BCK/9USC3/WUwx/2RRNP9jTjD/nJN+//7++f/9/f7//f39//7//v/8/f3//f36/9jUyv+ej3f/oo5v/6ONcf+fi2//ppmC/+Ph3f/X2dL/opB3/5yGaf+TgWP/inhc/5yLeP+Jd1//dmlN/3FiRv9uXD7/aFc5/1xQNP9TRyz/T0Ep/1VKLf9ZSy7/XE0x/4Z4YP+IfWf/r6qd//z8+//8/P3//f37///////n5+T/ppuI/5yLcP+hi27/nIhu/52Lbf+hkHf/3tzS/+7w7v+ypJH/nohp/4p2Wf+3q5r/+fTy/9HIv/91ZEb/eWZH/3BdQP9rWTz/XlAz/1RILP9PQij/V0wu/0tAJ/+0rqP////////////r6ef/2dXT//7+/v/8/v3/0s7G/+7r5//w8Ov/nI56/8S8rP/s6uD/ppZ8/5eDaP/Y1Mv/9/r6/8vAs/+Kd2D/vK2f//f49P/y8/D/6efk/4V2W/93YkL/dV9D/2tXO/9eTzL/V0ou/1BEKP9OQiT/fHJh///+/f/8/v7/+vz7///////e29f/zMjA///////NyMD/urSl//P08f/p5uD//P79/+/q5v+Zh3D/wbem//T08v/0+Pb/5d7W/8W8sf/4/Pj/6+ro/9XRyP/7/v7/n5SD/29cPv9zYkX/bFk8/2JSNf9ZTC//UkYq/0o+IP+8t6r///////v6+////vz/+v7+//X29v+Kfmz/vLSm///////Kxb7/1NDJ///////X08n/jXth/8W6p//8/f//9vf5//b39v/2+PX//f////T18P+onoz/o5iE/////v/Iwbv/c2BE/3RjRf9sWj3/YlM2/1hNMP9RRSn/Sz0j/4mDcv//////+/v8//n6+P/+////6+nl/4t7Yv+Aclb/y8e8///////8/Pz/+vz+/6+gkP/Duqr///////r8/P/8/Pz/+fr6//z////x8u7/qJ6N/49+YP+HeV3/3NrR/+zp5f92aE7/dGFD/2tYPP9fUDT/Vkou/1FFKf9SQiv/UEUr/8nHu////////f7+/////f+mnYr/fW5S/4h7X/+MfmX/2NbL/+Dh3v/39/X/6+3p//r7+v/9/P7//v7+//z8/P/+////9PLs/6qfif+QfV//jXxe/4JzWP+YjXj/m5B//3VkSv9wXkH/ZVQ3/1pNMf9TRyv/T0Mo/1NGKv9WSSv/XFI5/5GJdv+noJD/hXtn/25fQv9+b1b/g3Na/418Yv+JemX/i4Bt/9XSyf//////+fz7//7+/v/8/P3//////+/u6f+mmIL/kYJd/456Vv+HdFL/gnBT/3pnSv90ZUn/cmRI/2hbQP9gVDj/WU0x/1RGLv9PQir/TkQl/1NHLP9XTDD/V0or/15MLP9nVjj/cGNJ/3hrUv+AcFb/hXdh/6adkP/Jwrb/w760/+Ph3f//////+/v6///////n5d//npN5/5F7Yf+GeWH/jIBj/4h4WP96ak3/dGVI/3FkSv9rXET/ZFY+/1tPNf9WSTD/UEIr/0w/KP9LPiX/UEMo/1VJLf9dUTT/ZVc7/2ZYQP9oW0b/eGlR/3lqUv+fmov/+fr4////////////4uDf/+bl5P//////7+3r/5OKef+LfWD/iXdc/5qRgv/u7ub/ubKh/29hRP9wY0b/a11F/2hYQv9gUDv/V0kz/1NFLv9OQCr/Sz0n/0U3JP9LPSX/UEIp/1dILv9YSzL/XlE7/2VYQv9zY03/e21Y/+Lg2///////+/v7//39/v//////xcG+/9/c2P/+////ubKp/4R0Yf+on4z/+Pn0//v6+/+ck4b/bV1E/2haQv9kVj//YFI7/1tMNv9URS//T0Ar/0k6J/9FNyX/RDUk/0g5J/9MPSr/U0Qw/1RFMf9ZSjf/YFNA/2lbRP9/cl//8fDt//7+///9/f3//fz8///////V0cz/iH1s/+Ph3P//////0MzI//f29P/v7+z/lYuA/21dR/9pWkb/Xk88/2BRPf9cTTr/V0k1/1JEMP9NPiv/Rjgl/0I0Iv9AMiH/RTYm/0g5KP9PPy3/UEAv/1VENP9bTDv/ZlZC/2tdS//X1tD///////v7/P/9/f7//////62mmv9zZU//iYJ0/+3t6v//////8/Hv/4yDc/9oWUX/bFpH/2FRQ/9bSjr/WEg3/1VFNP9QQS//Sjwr/0g6J/9ENiP/PC8d/zouHP8/MSD/RDYj/0o9Kf9MPCr/T0Av/1dHN/9dTjv/YVNA/4eAdP/m5eH//P38//n7+f+3taz/aF5M/2teS/9pXEr/g3pr/8fDuv+LgnX/aVlG/2VURP9fTz7/Wkw6/1RFNP9URTP/UEEw/0w9LP9FNyX/QTMg/z8yH/82Khj/MSkY/zYuHP88MB//QTcl/0Y4Jv9HOyn/UEMy/1VHNP9aSzj/XlJB/2liUv+De27/e3Fk/1xRP/9cTjz/Wkw6/11POv9iVED/XE8+/15RQf9fUT//WUo5/1dKOP9TRjT/T0Ev/09BL/9KPSr/RDgm/0E1I/85LRv/NSoY/zEnFf8rKBb/LysZ/zUtHP85MiD/PjMh/z83JP9HPSv/UUMx/1VGM/9XSzj/WE89/1RIN/9YSDj/Wks5/1VHNf9URjT/UkUx/1NFMv9YSzr/Vko5/1NINf9PQzH/T0Mx/1BEMv9NPy3/SDso/0I4JP89NSL/OTEf/zQtGv8uJxX/LCUU/ykjEf8rJRT/MScZ/zErHP82LR7/Misa/y4nFf9EOyn/UEMx/1JDM/9PRTb/TUEw/1FDMf9RQjD/TD4q/0k7Kv9JPCr/Rzoo/0k8K/9JQDD/Rz4t/0Y8Kv9GOir/STwr/0U7J/8/NSP/NzAf/zQuHf8xLBr/LSgW/yokE/8mHxH/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="
j2y_version = "1.0.3.20200117.1"
project_site = "http://benzenpenxil.xyz/json2yaml-for-dice/"

#class type_system_info:
#    def __init__(self, name):
#        self.name = name
#
#system_info = type_system_info(os.name)

class type_deck:
    def __init__(self, name, author, version, command, desc, includes, info, default):
        self.name = name
        self.author = author
        self.version = version
        self.command = command
        self.desc = desc
        self.includes = includes
        self.info = info
        self.default = default

deck = type_deck("","","","","",[],"","")

#测试用代码
#deck.name = "彩六干员"
#deck.author = "仑质"
#deck.version = "191230"
#deck.command = "彩六干员"
#deck.desc = "抽取彩六干员"
#deck.includes = ["干员档案","干员性别"]
#deck.info = "牌堆转换器测试用"
#deck.default = "干员档案"
#s_tmp = "🕷️"
#print(s_tmp[1].encode("UTF-8"))
#print(len(s_tmp))

input_file_name = ""
output_file_name = ""
output_file_name += deck.command

def filter_emoji(desstr, restr="[EMOJI]"):
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)

def item_tran(item_this):
    item_this_new=""
    for i in range(0, len(item_this)):
        if item_this[i] == "{":
            if i + 1 <= len(item_this):
                if item_this[i + 1] != "%":
                    item_this_new += "{%"
                else:
                    item_this_new += "{$"
        elif item_this[i] == "%":
            if i - 1 >= 0:
                if item_this[i - 1] == "{":
                    pass
                else:
                    item_this_new += item_this[i]
            else:
                item_this_new += item_this[i]
        elif item_this[i] == "\n":
            item_this_new += "\\n"
        elif item_this[i] == ",":
            item_this_new += "，"
        else:
            item_this_new += item_this[i]
    return item_this_new

def item_tran2show(item_this):
    item_this_new = ""
    for i in range(0, len(item_this)):
        if item_this[i] == "\n":
            item_this_new += "\\n"
        elif item_this[i] == ",":
            item_this_new += "，"
        else:
            item_this_new += item_this[i]
    item_this_new = filter_emoji(item_this_new)
    return item_this_new

def json2yaml_work():
    global deck
    global input_file_name
    global output_file_name
    global root
    global progress_obj
    progress_obj["value"] = 0
    root.update()
    output_str = "#必要信息\nname: " + deck.name
    output_str += "\nauthor: " + deck.author
    output_str += "\nversion: " + deck.version
    output_str += "\ncommand: " + deck.command
    output_str += "\ndesc: " + deck.desc
    if deck.includes != [""]:
        deck.includes_str = ""
        for str_now in deck.includes:
            deck.includes_str += "  - \"" + str_now + "\"\n"
        output_str += "\nincludes:\n" + deck.includes_str
    else:
        output_str += "\n"
    #output_str += "\n#作者信息\n_version:\n  - \"" + deck.version + "\""
    #output_str += "\n_author:\n  - \"" + deck.author + "\""
    #output_str += "\ninfo:\n  - \"" + deck.info + "\"\n"
    output_str += "\n#牌堆部分\n"
    progress_obj["value"] = 5
    root.update()

    try:
        with open(input_file_name,"r",encoding="utf-8") as input_file_obj:
            input_str = input_file_obj.read()
            if input_str.startswith(codecs.BOM_UTF8.decode("UTF-8")):
                input_dict = json.loads(input_str[1:], encoding="utf-8")
            else:
                input_dict = json.loads(input_str, encoding="utf-8")
            progress_obj["value"] = 10
            root.update()
    except json.decoder.JSONDecodeError as error_info:
        input_file_name = ""
        file_name_str.set(file_name_head + "请确保文件的Json格式没有错误")
        tkinter.messagebox.showerror("json.decoder.JSONDecodeError", error_info)
        progress_obj["value"] = 0
        root.update()
    except UnicodeDecodeError as error_info:
        input_file_name = ""
        file_name_str.set(file_name_head + "请确保文件编码格式是UTF-8")
        tkinter.messagebox.showerror("UnicodeDecodeError", error_info)
        progress_obj["value"] = 0
        root.update()
    else:
        if deck.default in input_dict:
            output_str += "default:\n"
            for item_this in input_dict.get(deck.default):
                item_this = item_tran(item_this)
                output_str += "  - \"" + item_this + "\"\n"
        progress_obj["value"] = 15
        root.update()
        count_work = 0
        for key_this in list(input_dict.keys()):
            count_work += len(input_dict.get(key_this)) + 1
        if count_work <= 75:
            count_step = 1
        else:
            count_step = int(count_work / 75)
        id_count_all = 0
        for key_this in list(input_dict.keys()):
            output_str += key_this + ":\n"
            id_count_all += 1
            progress_obj["value"] = int(id_count_all * 75 / count_work + 15)
            root.update()
            for item_this in input_dict.get(key_this):
                item_this = item_tran(item_this)
                output_str += "  - \"" + item_this + "\"\n"
                id_count_all += 1
                if id_count_all % (count_step) == 0:
                    progress_obj["value"] = int(id_count_all * 75 / count_work + 15)
                    root.update()

    with open(output_file_name, "w", encoding="utf-8") as output_file_obj:
        output_file_obj.write(output_str)
    progress_obj["value"] = 100
    root.update()

def select_file():
    global file_name_str
    global tree
    global input_file_name
    global root
    global progress_obj
    progress_obj["value"] = 0
    root.update()
    file_name = tkinter.filedialog.askopenfilenames(title="请选择Json文件", filetypes=[("Json", "*.json"), ("All Files", "*")])
    progress_obj["value"] = 5
    root.update()
    if len(file_name) == 1:
        for file_name_now in file_name:
            try:
                with open(file_name_now,"r",encoding="utf-8") as input_file_obj:
                    input_str = input_file_obj.read()
                    if input_str.startswith(codecs.BOM_UTF8.decode("UTF-8")):
                        input_dict = json.loads(input_str[1:], encoding="utf-8")
                    else:
                        input_dict = json.loads(input_str, encoding="utf-8")
                progress_obj["value"] = 25
                root.update()
            except json.decoder.JSONDecodeError as error_info:
                input_file_name = ""
                file_name_str.set(file_name_head + "请确保文件的Json格式没有错误")
                tkinter.messagebox.showerror("json.decoder.JSONDecodeError", error_info)
                progress_obj["value"] = 0
                root.update()
            except UnicodeDecodeError as error_info:
                input_file_name = ""
                file_name_str.set(file_name_head + "请确保文件编码格式是UTF-8")
                tkinter.messagebox.showerror("UnicodeDecodeError", error_info)
                progress_obj["value"] = 0
                root.update()
            else:
                count_work = 0
                for key_this in list(input_dict.keys()):
                    count_work += len(input_dict.get(key_this)) + 1
                input_file_name = file_name_now
                file_name_str.set(file_name_head + "\"" + file_name_now + "\"")
                if len(tree.get_children()) != 0:
                    for tree_children_now in tree.get_children():
                        tree.delete(tree_children_now)
                if count_work <= 75:
                    count_step = 1
                else:
                    count_step = int(count_work / 75)
                tree_id_0_count = 0
                tree_id_all_count = 0
                for key_this in list(input_dict.keys()):
                    tree_id_0 = tree.insert("", tree_id_0_count, key_this + "#" + str(tree_id_all_count), text=key_this, value=str(tree_id_all_count))
                    tree_id_all_count += 1
                    tree_id_1_count = 0
                    progress_obj["value"] = int(tree_id_all_count * 75 / count_work + 25)
                    root.update()
                    for item_this in input_dict.get(key_this):
                        item_this = item_tran2show(item_this)
                        tree_id_1 = tree.insert(tree_id_0, tree_id_1_count, item_this + "#" + str(tree_id_all_count), text=item_this, value=str(tree_id_all_count))
                        tree_id_all_count += 1
                        tree_id_1_count += 1
                        if tree_id_all_count % (count_step) == 0:
                            progress_obj["value"] = int(tree_id_all_count * 75 / count_work + 25)
                            root.update()
                        #print(tree_id_all_count)
                    tree_id_0_count += 1
                progress_obj["value"] = 100
                root.update()
                #print(tree_id_all_count)
                #print(tree.get_children())
    elif len(file_name) == 0:
        if len(input_file_name) == 0:
            file_name_str.set(file_name_head + "请选择文件！")
        tkinter.messagebox.showwarning("警告", "请选择文件！")
        progress_obj["value"] = 0
        root.update()
    else:
        if len(input_file_name) == 0:
            file_name_str.set(file_name_head + "请一次只选择一个文件！")
        tkinter.messagebox.showwarning("警告", "请一次只选择一个文件！")
        progress_obj["value"] = 0
        root.update()

def tran_save():
    global t1
    global t2
    global t3
    global t4
    global t5
    global t6
    global deck
    global input_file_name
    global output_file_name
    global root
    #file_name = tkinter.filedialog.asksaveasfilename(initialdir = "./test")
    if len(input_file_name) != 0:
        file_path = tkinter.filedialog.askdirectory(title="选择保存路径")
        if len(file_path) != 0:
            #print(file_path)
            deck.name = t1.get()
            deck.author = t2.get()
            deck.version = t3.get()
            deck.command = t1.get()
            deck.desc = t4.get()
            deck.includes = t5.get().split(",")
            deck.default = t6.get()
            output_file_name = file_path + "/" + deck.name
            #print(deck.includes)
            json2yaml_work()
            tkinter.messagebox.showinfo("完成","已保存到 " + output_file_name)
        else:
            tkinter.messagebox.showwarning("警告", "请选择保存路径！")
            progress_obj["value"] = 0
            root.update()
    else:
        tkinter.messagebox.showwarning("警告", "请先选择要转换的Json文件！")
        progress_obj["value"] = 0
        root.update()

def show_info():
    tkinter.messagebox.showinfo("Json2Yaml By BenzenPenxil","Json2Yaml基于Python\n\n项目主页：\n" + project_site + "\n\n作者：仑质(BenzenPenxil)\n版本：" + j2y_version + "\n有问题请联系QQ：137334701")

def show_project_site():
    tkinter.messagebox.showinfo("提示", "将通过浏览器访问 " + project_site)
    try:
        webbrowser.open(project_site)
    except webbrowser.Error as error_info:
        tkinter.messagebox.showerror("webbrowser.Error", error_info)

if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Json2Yaml By BenzenPenxil")
    root.geometry("560x624")
    root.resizable(width=False, height=False)

    file_name_head = "Json文件路径："
    file_name_str = tkinter.StringVar()
    file_name_str.set(file_name_head + "请选择文件！")
    L1 = tkinter.Label(root, textvariable = file_name_str)
    L1.place(x=0, y=0, width=560,height=32)

    EtL1 = tkinter.Label(root, text = "名称/命令")
    EtL1.place(x=0, y=432, width=60,height=32)
    t1 = tkinter.StringVar()
    t1.set("名称与命令")
    Et1 = tkinter.Entry(root, textvariable=t1)
    Et1.place(x=60, y=432, width=500, height=32)

    EtL2 = tkinter.Label(root, text = "作者")
    EtL2.place(x=0, y=464, width=60,height=32)
    t2 = tkinter.StringVar()
    t2.set("作者")
    Et2 = tkinter.Entry(root, textvariable=t2)
    Et2.place(x=60, y=464, width=500, height=32)

    EtL3 = tkinter.Label(root, text = "版本")
    EtL3.place(x=0, y=496, width=60,height=32)
    t3 = tkinter.StringVar()
    t3.set("版本")
    Et3 = tkinter.Entry(root, textvariable=t3)
    Et3.place(x=60, y=496, width=500, height=32)

    EtL4 = tkinter.Label(root, text = "描述")
    EtL4.place(x=0, y=528, width=60,height=32)
    t4 = tkinter.StringVar()
    t4.set("描述")
    Et4 = tkinter.Entry(root, textvariable=t4)
    Et4.place(x=60, y=528, width=500, height=32)

    EtL5 = tkinter.Label(root, text = "子指令")
    EtL5.place(x=0, y=560, width=60,height=32)
    t5 = tkinter.StringVar()
    t5.set("子指令")
    Et5 = tkinter.Entry(root, textvariable=t5)
    Et5.place(x=60, y=560, width=500, height=32)

    EtL6 = tkinter.Label(root, text = "Default")
    EtL6.place(x=0, y=592, width=60,height=32)
    t6 = tkinter.StringVar()
    t6.set("Default")
    Et6 = tkinter.Entry(root, textvariable=t6)
    Et6.place(x=60, y=592, width=500, height=32)

    #Btn1 = tkinter.Button(root, text = "选择文件", command = select_file)
    #Btn1.place(x=500, y=0, width=60, height=32)
    #Btn2 = tkinter.Button(root, text="开始转换", command = tran_save)
    #Btn2.place(x=500, y=592, width=60, height=32)
    #Btn3 = tkinter.Button(root, text="i", command = show_info)
    #Btn3.place(x=528, y=432, width=32, height=32)

    menu_bar = tkinter.Menu(root)
    file_menu = tkinter.Menu(menu_bar, tearoff=0)
    info_menu = tkinter.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="文件", menu=file_menu)
    menu_bar.add_cascade(label="关于", menu=info_menu)
    file_menu.add_command(label="导入文件", command=select_file)
    file_menu.add_command(label="开始转换", command=tran_save)
    info_menu.add_command(label="关于", command=show_info)
    info_menu.add_command(label="查看项目", command=show_project_site)
    root.config(menu=menu_bar)

    t1.set("填入牌堆名，这同时也将是该牌堆的对应指令")
    t2.set("填入作者")
    t3.set("填入版本号")
    t4.set("填入对于该牌堆的描述")
    t5.set(",".join(["填入子指令并用半角逗号隔开"]))
    t6.set("要设置子指令缺省时的调用项请设置此项")

    #测试用
    #t1.set(deck.name)
    #t2.set(deck.author)
    #t3.set(deck.version)
    #t4.set(deck.desc)
    #t5.set(",".join(deck.includes))
    #t6.set(deck.default)

    tree = ttk.Treeview(root)
    tree.place(x=0, y=32, width=560, height=400)

    progress_obj = ttk.Progressbar(root, orient="horizontal", length=560, mode="determinate")
    progress_obj.place(x=0, y=32, width=560, height=25)
    progress_obj["maximum"] = 100
    progress_obj["value"] = 0

    with open("tmp.ico", "wb+") as tmp:
        tmp.write(base64.b64decode(favicon_ico))
    root.iconbitmap("tmp.ico")
    os.remove("tmp.ico")
    root.mainloop()
    #json2yaml_work()

