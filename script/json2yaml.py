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
import pyperclip

from j2y_data import *

j2y_version = "1.0.9.20200605.1"
project_site = "http://benzenpenxil.xyz/json2yaml-for-dice/"

#class type_system_info:
#    def __init__(self, name):
#        self.name = name
#
#system_info = type_system_info(os.name)

class type_deck:
    def __init__(self, name, author, version, command, desc, includes, info, default, import_list):
        self.name = name
        self.author = author
        self.version = version
        self.command = command
        self.desc = desc
        self.includes = includes
        self.info = info
        self.default = default
        self.import_list = import_list

deck = type_deck("","","","","",[],"","",[])

#测试用代码
#deck.name = "彩六干员"
#deck.author = "仑质"
#deck.version = "191230"
#deck.command = "彩六干员"
#deck.desc = "抽取彩六干员"
#deck.includes = ["干员档案","干员性别"]
#deck.info = "牌堆转换器测试用"
#deck.default = "干员档案"

input_file_name = ""
output_file_name = ""
output_file_name += deck.command

giveback_flag = 0
versiontran_flag = 0
tabtran_flag = 0
infoadd_flag = 1
import_flag = 1

dict_import_default = {"性别": ["男", "女", "不明"]}
dict_import_default.update(dict_from_shiki)
dict_for_import = {}
dict_for_import.update(dict_import_default)
#dict_for_import.update({"测试": ["测试"]})
list_for_import_record = []

def filter_emoji(desstr, restr="[EMOJI]"):
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)

def item_get_import_list(dict_this):
    output_list = []
    for key_this in list(dict_this.keys()):
        for item_this in dict_this.get(key_this):
            for in_item_key_this in re.finditer("\{%{0,1}(.*?)\}", item_this):
                in_item_key_this_str = in_item_key_this.group().lstrip("{").lstrip("%").rstrip("}")
                if in_item_key_this_str.find("{") < 0 and in_item_key_this_str.find("}") < 0:
                    if in_item_key_this_str in list(dict_this.keys()):
                        pass
                    else:
                        if in_item_key_this_str in output_list:
                            pass
                        else:
                            output_list.append(in_item_key_this_str)
    return output_list

def str_get_import_list(str_this, dict_this):
    global list_for_import_record
    output_list = []
    for in_item_key_this in re.finditer("\{%{0,1}(.*?)\}", str_this):
        in_item_key_this_str = in_item_key_this.group().lstrip("{").lstrip("%").rstrip("}")
        if in_item_key_this_str not in list_for_import_record:
            if in_item_key_this_str.find("{") < 0 and in_item_key_this_str.find("}") < 0:
                if in_item_key_this_str in list(dict_this.keys()):
                    pass
                else:
                    if in_item_key_this_str in output_list:
                        pass
                    else:
                        output_list.append(in_item_key_this_str)
            list_for_import_record.append(in_item_key_this_str)
    return output_list

def item_tran(item_this, flag):
    dice_flag = 0
    item_this_new=""
    for i in range(0, len(item_this)):
        if item_this[i] == "{":
            if i + 1 <= len(item_this):
                if item_this[i + 1] != "%":
                    if flag == 0:
                        item_this_new += "{%"
                    else:
                        item_this_new += "{$"
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
        elif item_this[i] == "D":
            if dice_flag == 0:
                item_this_new += item_this[i]
            else:
                item_this_new += "d"
        elif item_this[i] == "[":
            dice_flag += 1
            item_this_new += item_this[i]
        elif item_this[i] == "]":
            dice_flag -= 1
            item_this_new += item_this[i]
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

def add_import_work(dict_need_import, dict_for_import, output_str, dict_this):
    global tabtran_flag
    global giveback_flag
    global list_for_import_record
    dict_need_import_next = []
    for key_this in dict_need_import:
        if key_this in list(dict_for_import.keys()):
            output_str += key_this + ":\n"
            if tabtran_flag != 0:
                output_tran_flag_tmp = 1
            for item_this in dict_for_import.get(key_this):
                dict_need_import_next += str_get_import_list(item_this, dict_this)
                item_this = item_tran(item_this, giveback_flag)
                if output_tran_flag_tmp == 0:
                    output_str += "  - \"" + item_this + "\"\n"
                else:
                    output_tran_flag_tmp = 0
                    output_str += "  - \" " + item_this + "\"\n"
    if dict_need_import_next != []:
        output_str = add_import_work(dict_need_import_next, dict_for_import, output_str, dict_this)
    return output_str

def json2yaml_work():
    global giveback_flag
    global versiontran_flag
    global infoadd_flag
    global import_flag
    global deck
    global input_file_name
    global output_file_name
    global root
    global progress_obj
    global list_for_import_record
    progress_obj["value"] = 0
    root.update()
    output_str = "#必要信息\nname: " + deck.name
    output_str += "\nauthor: " + deck.author
    output_str += "(使用Json2Yaml转换生成)"
    output_str += "\nversion: "
    if versiontran_flag == 0:
        output_str += deck.version
    else:
        output_str += deck.version.replace(".", "_")
    output_str += "\ncommand: " + deck.command
    output_str += "\ndesc: " + deck.desc
    if deck.includes != [""]:
        deck.includes_str = ""
        for str_now in deck.includes:
            deck.includes_str += "  - \"" + str_now + "\"\n"
        output_str += "\nincludes:\n" + deck.includes_str
    else:
        output_str += "\n"
    if infoadd_flag != 0:
        output_str += "\n#作者信息\ninfo:\n  - \"" + "本牌堆使用Json2Yaml(By BenzenPenxil)自动转换生成\\n转换器版本号：" + j2y_version + "\\n牌堆原作者：" + deck.author + "\"\n"
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
        output_tran_flag_tmp = 0
        if deck.default in input_dict:
            output_str += "default:\n"
            if tabtran_flag != 0:
                output_tran_flag_tmp = 1
            for item_this in input_dict.get(deck.default):
                item_this = item_tran(item_this, giveback_flag)
                if output_tran_flag_tmp == 0:
                    output_str += "  - \"" + item_this + "\"\n"
                else:
                    output_tran_flag_tmp = 0
                    output_str += "  - \" " + item_this + "\"\n"
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
            if tabtran_flag != 0:
                output_tran_flag_tmp = 1
            for item_this in input_dict.get(key_this):
                item_this = item_tran(item_this, giveback_flag)
                if output_tran_flag_tmp == 0:
                    output_str += "  - \"" + item_this + "\"\n"
                else:
                    output_tran_flag_tmp = 0
                    output_str += "  - \" " + item_this + "\"\n"
                id_count_all += 1
                if id_count_all % (count_step) == 0:
                    progress_obj["value"] = int(id_count_all * 75 / count_work + 15)
                    root.update()
        if import_flag != 0:
            list_for_import_record = []
            dict_need_import_next = []
            deck.import_list = item_get_import_list(input_dict)
            deck_import_list = deck.import_list.copy()
            for key_this in deck_import_list:
                if key_this in list(dict_for_import.keys()):
                    deck.import_list.remove(key_this)
                    output_str += key_this + ":\n"
                    if tabtran_flag != 0:
                        output_tran_flag_tmp = 1
                    for item_this in dict_for_import.get(key_this):
                        dict_need_import_next += str_get_import_list(item_this, input_dict)
                        item_this = item_tran(item_this, giveback_flag)
                        if output_tran_flag_tmp == 0:
                            output_str += "  - \"" + item_this + "\"\n"
                        else:
                            output_tran_flag_tmp = 0
                            output_str += "  - \" " + item_this + "\"\n"
            if dict_need_import_next != []:
                output_str = add_import_work(dict_need_import_next, dict_for_import, output_str, input_dict)
            if len(deck.import_list) != 0:
                tkinter.messagebox.showwarning("未解决的依赖项", "以下依赖项未找到:\n - " + "\n - ".join(deck.import_list) + "\n将会导致抽取时无法正常调用。")

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
                if import_flag != 0:
                    import_list_tmp = item_get_import_list(input_dict)
                    #print("|".join(import_list_tmp))
                    if len(import_list_tmp) != 0:
                        tkinter.messagebox.showwarning("存在依赖项", "扫描中发现以下被引用项不包含于导入文件中:\n - " + "\n - ".join(import_list_tmp) + "\n请确保可以提供这些依赖项。" )
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
            try:
                deck.name = t1.get()
                deck.author = t2.get()
                deck.version = t3.get()
                deck.command = t1.get()
                deck.desc = t4.get()
                deck.includes = t5.get().split(",")
                deck.default = t6.get()
            except UnicodeDecodeError as error_info:
                tkinter.messagebox.showerror("UnicodeDecodeError", error_info)
                progress_obj["value"] = 0
                root.update()
            else:
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

def load_import():
    global dict_for_import
    global dict_import_default
    input_file_name = ""
    progress_obj["value"] = 0
    root.update()
    file_name = tkinter.filedialog.askopenfilenames(title="请选择Json文件", filetypes=[("Json", "*.json"), ("All Files", "*")])
    progress_obj["value"] = 5
    root.update()
    if len(file_name) > 0:
        count_error = 0
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
                #tkinter.messagebox.showerror("json.decoder.JSONDecodeError", error_info)
                count_error += 1
                progress_obj["value"] = 0
                root.update()
            except UnicodeDecodeError as error_info:
                input_file_name = ""
                file_name_str.set(file_name_head + "请确保文件编码格式是UTF-8")
                #tkinter.messagebox.showerror("UnicodeDecodeError", error_info)
                count_error += 1
                progress_obj["value"] = 0
                root.update()
            else:
                dict_for_import.update(**input_dict)
                dict_for_import.update(**dict_import_default)
                #dict_for_import = {**dict_for_import, **input_dict}
                #print(len(dict_for_import))
                progress_obj["value"] = 100
                root.update()
        tkinter.messagebox.showinfo("依赖项已更新", "当前已载入" + str(len(dict_for_import)) + "个备用依赖项\n尝试载入" + str(len(file_name)) + "个文件\n其中共有" + str(count_error) + "个加载失败")
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

def clear_conf():
    global t1
    global t2
    global t3
    global t4
    global t5
    global t6
    t1.set("")
    t2.set("")
    t3.set("")
    t4.set("")
    t5.set("")
    t6.set("")

def giveback_switch():
    global giveback_flag
    global root
    global set_menu
    if giveback_flag == 0:
        giveback_flag = 1
        set_menu.entryconfig(1, label="忽略不放回[√]")
    else:
        giveback_flag = 0
        set_menu.entryconfig(1, label="忽略不放回[×]")
    #print(str(giveback_flag))

def versiontran_switch():
    global versiontran_flag
    global root
    global set_menu
    if versiontran_flag == 0:
        versiontran_flag = 1
        set_menu.entryconfig(2, label="版本号优化[√]")
    else:
        versiontran_flag = 0
        set_menu.entryconfig(2, label="版本号优化[×]")

def tabtran_switch():
    global tabtran_flag
    global root
    global set_menu
    if tabtran_flag == 0:
        tabtran_flag = 1
        set_menu.entryconfig(3, label="排版格式优化[√]")
    else:
        tabtran_flag = 0
        set_menu.entryconfig(3, label="排版格式优化[×]")

def infoadd_switch():
    global infoadd_flag
    global root
    global set_menu
    if infoadd_flag == 0:
        infoadd_flag = 1
        set_menu.entryconfig(4, label="附加Info项[√]")
    else:
        infoadd_flag = 0
        set_menu.entryconfig(4, label="附加Info项[×]")

def import_switch():
    global import_flag
    global root
    global set_menu
    if import_flag == 0:
        import_flag = 1
        set_menu.entryconfig(5, label="尝试解决依赖项[√]")
    else:
        import_flag = 0
        set_menu.entryconfig(5, label="尝试解决依赖项[×]")

def show_info():
    tkinter.messagebox.showinfo("Json2Yaml By BenzenPenxil","Json2Yaml基于Python\n\n项目主页：\n" + project_site + "\n\n作者：仑质(BenzenPenxil)\n版本：" + j2y_version + "\n有问题请联系QQ：137334701")

def show_project_site():
    tkinter.messagebox.showinfo("提示", "将通过浏览器访问 " + project_site)
    try:
        webbrowser.open(project_site)
    except webbrowser.Error as error_info:
        tkinter.messagebox.showerror("webbrowser.Error", error_info)

def tree_copy(obj, event=None):
    length_select = len(obj.selection())
    if length_select != 0:
        str_select = obj.selection()[0]
        str_select_len = len(str_select)
        for i in range(1, str_select_len):
            if str_select[-i] == "#":
                pyperclip.copy(str_select[-str_select_len: - i])
                break

def tree_set_name(obj, event=None):
    global t1
    length_select = len(obj.selection())
    if length_select != 0:
        str_select = obj.selection()[0]
        str_select_len = len(str_select)
        for i in range(1, str_select_len):
            if str_select[-i] == "#":
                t1.set(str_select[-str_select_len: - i])
                break

def tree_add_includes(obj, event=None):
    global t5
    length_select = len(obj.selection())
    if length_select != 0:
        str_select = obj.selection()[0]
        str_select_len = len(str_select)
        for i in range(1, str_select_len):
            if str_select[-i] == "#":
                if t5.get().split(",") != [""]:
                    if str_select[-str_select_len: - i] in t5.get().split(","):
                        pass
                    else:
                        tmp_t5_str = t5.get().split(",")
                        tmp_t5_str.append(str_select[-str_select_len: - i])
                        t5.set(",".join(tmp_t5_str))
                else:
                    t5.set(str_select[-str_select_len: - i])
                break

def tree_set_default(obj, event=None):
    global t5
    global t6
    length_select = len(obj.selection())
    if length_select != 0:
        str_select = obj.selection()[0]
        str_select_len = len(str_select)
        for i in range(1, str_select_len):
            if str_select[-i] == "#":
                t6.set(str_select[-str_select_len: - i])
                if t5.get().split(",") != [""]:
                    if "default" in t5.get().split(","):
                        pass
                    else:
                        tmp_t5_str = t5.get().split(",")
                        tmp_t5_str.append("default")
                        t5.set(",".join(tmp_t5_str))
                else:
                    t5.set("default")
                break

def tree_rightKey(event, obj):
    tree_rightkey_menu.delete(0, tkinter.END)
    tree_rightkey_menu.add_command(label="复制", command=lambda: tree_copy(obj, event))
    tree_rightkey_menu.add_command(label="设为名称/指令", command=lambda: tree_set_name(obj, event))
    tree_rightkey_menu.add_command(label="加入子指令", command=lambda: tree_add_includes(obj, event))
    tree_rightkey_menu.add_command(label="设为default", command=lambda: tree_set_default(obj, event))
    tree_rightkey_menu.post(event.x_root, event.y_root)

def entry_cut(editor, event=None):
    editor.event_generate("<<Cut>>")

def entry_copy(editor, event=None):
    editor.event_generate("<<Copy>>")

def entry_paste(editor, event=None):
    editor.event_generate('<<Paste>>')

def entry_clear(editor, event=None):
    global root
    root.globalsetvar(editor["textvariable"], "")

def entry_rightKey(event, editor):
    entry_rightkey_menu.delete(0, tkinter.END)
    entry_rightkey_menu.add_command(label='剪切', command=lambda: entry_cut(editor))
    entry_rightkey_menu.add_command(label='复制', command=lambda: entry_copy(editor))
    entry_rightkey_menu.add_command(label='粘贴', command=lambda: entry_paste(editor))
    entry_rightkey_menu.add_command(label='清空', command=lambda: entry_clear(editor))
    entry_rightkey_menu.post(event.x_root,event.y_root)

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

    entry_rightkey_menu = tkinter.Menu(root,tearoff=False)

    EtL1 = tkinter.Label(root, text = "名称/指令")
    EtL1.place(x=0, y=432, width=60,height=32)
    t1 = tkinter.StringVar()
    t1.set("名称与指令")
    Et1 = tkinter.Entry(root, textvariable=t1)
    Et1.place(x=60, y=432, width=500, height=32)
    Et1.bind("<Button-3>", lambda x: entry_rightKey(x, Et1))

    EtL2 = tkinter.Label(root, text = "作者")
    EtL2.place(x=0, y=464, width=60,height=32)
    t2 = tkinter.StringVar()
    t2.set("作者")
    Et2 = tkinter.Entry(root, textvariable=t2)
    Et2.place(x=60, y=464, width=500, height=32)
    Et2.bind("<Button-3>", lambda x: entry_rightKey(x, Et2))

    EtL3 = tkinter.Label(root, text = "版本")
    EtL3.place(x=0, y=496, width=60,height=32)
    t3 = tkinter.StringVar()
    t3.set("版本")
    Et3 = tkinter.Entry(root, textvariable=t3)
    Et3.place(x=60, y=496, width=500, height=32)
    Et3.bind("<Button-3>", lambda x: entry_rightKey(x, Et3))

    EtL4 = tkinter.Label(root, text = "描述")
    EtL4.place(x=0, y=528, width=60,height=32)
    t4 = tkinter.StringVar()
    t4.set("描述")
    Et4 = tkinter.Entry(root, textvariable=t4)
    Et4.place(x=60, y=528, width=500, height=32)
    Et4.bind("<Button-3>", lambda x: entry_rightKey(x, Et4))

    EtL5 = tkinter.Label(root, text = "子指令")
    EtL5.place(x=0, y=560, width=60,height=32)
    t5 = tkinter.StringVar()
    t5.set("子指令")
    Et5 = tkinter.Entry(root, textvariable=t5)
    Et5.place(x=60, y=560, width=500, height=32)
    Et5.bind("<Button-3>", lambda x: entry_rightKey(x, Et5))

    EtL6 = tkinter.Label(root, text = "Default")
    EtL6.place(x=0, y=592, width=60,height=32)
    t6 = tkinter.StringVar()
    t6.set("Default")
    Et6 = tkinter.Entry(root, textvariable=t6)
    Et6.place(x=60, y=592, width=500, height=32)
    Et6.bind("<Button-3>", lambda x: entry_rightKey(x, Et6))

    #Btn1 = tkinter.Button(root, text = "选择文件", command = select_file)
    #Btn1.place(x=500, y=0, width=60, height=32)
    #Btn2 = tkinter.Button(root, text="开始转换", command = tran_save)
    #Btn2.place(x=500, y=592, width=60, height=32)
    #Btn3 = tkinter.Button(root, text="i", command = show_info)
    #Btn3.place(x=528, y=432, width=32, height=32)

    menu_bar = tkinter.Menu(root)
    file_menu = tkinter.Menu(menu_bar, tearoff=0)
    set_menu = tkinter.Menu(menu_bar, tearoff=0)
    info_menu = tkinter.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="文件", menu=file_menu)
    menu_bar.add_cascade(label="操作", menu=set_menu)
    menu_bar.add_cascade(label="关于", menu=info_menu)
    file_menu.add_command(label="导入文件", command=select_file)
    file_menu.add_command(label="开始转换", command=tran_save)
    file_menu.add_command(label="加载依赖项", command=load_import)
    set_menu.add_command(label="清空所有设置栏", command=clear_conf)
    set_menu.add_command(label="忽略不放回[×]", command=giveback_switch)
    set_menu.add_command(label="版本号优化[√]", command=versiontran_switch)
    set_menu.add_command(label="排版格式优化[×]", command=tabtran_switch)
    set_menu.add_command(label="附加Info项[√]", command=infoadd_switch)
    set_menu.add_command(label="尝试解决依赖项[√]", command=import_switch)
    info_menu.add_command(label="关于", command=show_info)
    info_menu.add_command(label="查看项目", command=show_project_site)
    root.config(menu=menu_bar)

    if giveback_flag != 0:
        set_menu.entryconfig(1, label="忽略不放回[√]")
    else:
        set_menu.entryconfig(1, label="忽略不放回[×]")
    if versiontran_flag != 0:
        set_menu.entryconfig(2, label="版本号优化[√]")
    else:
        set_menu.entryconfig(2, label="版本号优化[×]")
    if tabtran_flag != 0:
        set_menu.entryconfig(3, label="排版格式优化[√]")
    else:
        set_menu.entryconfig(3, label="排版格式优化[×]")
    if infoadd_flag != 0:
        set_menu.entryconfig(4, label="附加Info项[√]")
    else:
        set_menu.entryconfig(4, label="附加Info项[×]")
    if import_flag != 0:
        set_menu.entryconfig(5, label="尝试解决依赖项[√]")
    else:
        set_menu.entryconfig(5, label="尝试解决依赖项[×]")

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
    tree.place(x=0, y=32, width=545, height=401)
    tree_rightkey_menu = tkinter.Menu(root,tearoff=False)
    tree.bind("<Button-3>", lambda x: tree_rightKey(x, tree))

    progress_obj = ttk.Progressbar(root, orient="horizontal", length=560, mode="determinate")
    progress_obj.place(x=0, y=32, width=560, height=25)
    progress_obj["maximum"] = 100
    progress_obj["value"] = 0

    tree.columnconfigure(0, weight=1)

    tree_yscroll = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree_yscroll.place(x=544, y=57, width=16, height=375)
    tree.configure(yscrollcommand=tree_yscroll.set)

    with open("tmp.ico", "wb+") as tmp:
        tmp.write(base64.b64decode(favicon_ico))
    root.iconbitmap("tmp.ico")
    os.remove("tmp.ico")
    root.mainloop()
    #json2yaml_work()

