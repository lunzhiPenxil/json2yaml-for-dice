#!/usr/bin/env python37
# -*- encoding: utf-8 -*-
'''
@File    :   json2yaml_2.py
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
import re
import tkinter
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

j2y_version = "1.0.0.20200114.1"

#初始值测试用
deck_name = "彩六干员"
deck_author = "仑质"
deck_version = "191230"
deck_command = "彩六干员"
deck_desc = "抽取彩六干员"
deck_includes = ["干员档案","干员性别"]
deck_info = "牌堆转换器测试用"
deck_default = "干员档案"

input_file_name = ""
output_file_name = ""
output_file_name += deck_command

def json2yaml_work():
    global deck_name
    global deck_author
    global deck_version
    global deck_command
    global deck_desc
    global deck_includes
    global deck_info
    global deck_default
    global input_file_name
    global output_file_name
    output_str = "#必要信息\nname: " + deck_name
    output_str += "\nauthor: " + deck_author
    output_str += "\nversion: " + deck_version
    output_str += "\ncommand: " + deck_command
    output_str += "\ndesc: " + deck_desc
    if deck_includes != [""]:
        deck_includes_str = ""
        for str_now in deck_includes:
            deck_includes_str += "  - \"" + str_now + "\"\n"
        output_str += "\nincludes:\n" + deck_includes_str
        #print(str(deck_includes))
    else:
        output_str += "\n"
    #output_str += "\n#作者信息\n_version:\n  - \"" + deck_version + "\""
    #output_str += "\n_author:\n  - \"" + deck_author + "\""
    #output_str += "\ninfo:\n  - \"" + deck_info + "\"\n"
    output_str += "\n#牌堆部分\n"

    with open(input_file_name,"r",encoding="utf-8") as input_file_obj:
        input_str = input_file_obj.read()
        if input_str.startswith(codecs.BOM_UTF8.decode("UTF-8")):
            input_dict = json.loads(input_str[1:], encoding="utf-8")
        else:
            input_dict = json.loads(input_str, encoding="utf-8")
        if deck_default in input_dict:
            output_str += "default:\n"
            for item_this in input_dict.get(deck_default):
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
                item_this = item_this_new
                output_str += "  - \"" + item_this + "\"\n"
        for key_this in list(input_dict.keys()):
            output_str += key_this + ":\n"
            for item_this in input_dict.get(key_this):
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
                item_this = item_this_new
                output_str += "  - \"" + item_this + "\"\n"
    with open(output_file_name, "w", encoding="utf-8") as output_file_obj:
        output_file_obj.write(output_str)

def select_file():
    global file_name_str
    global tree
    global input_file_name
    file_name = tkinter.filedialog.askopenfilenames(title="请选择Json文件", filetypes=[("Json", "*.json"), ("All Files", "*")])
    if len(file_name) == 1:
        for file_name_now in file_name:
            #print(file_name_now)
            input_file_name = file_name_now
            file_name_str.set(file_name_head + "\"" + file_name_now + "\"")
            with open(file_name_now,"r",encoding="utf-8") as input_file_obj:
                input_str = input_file_obj.read()
                if input_str.startswith(codecs.BOM_UTF8.decode("UTF-8")):
                    input_dict = json.loads(input_str[1:], encoding="utf-8")
                else:
                    input_dict = json.loads(input_str, encoding="utf-8")
        if len(tree.get_children()) != 0:
            for tree_children_now in tree.get_children():
                tree.delete(tree_children_now)
        tree_id_0_count = 0
        tree_id_all_count = 0
        for key_this in list(input_dict.keys()):
            tree_id_0 = tree.insert("", tree_id_0_count, key_this + "#" + str(tree_id_all_count), text=key_this, value=str(tree_id_all_count))
            tree_id_all_count += 1
            tree_id_1_count = 0
            for item_this in input_dict.get(key_this):
                item_this_new = ""
                for i in range(0, len(item_this)):
                    if item_this[i] == "\n":
                        item_this_new += "\\n"
                    elif item_this[i] == ",":
                        item_this_new += "，"
                    else:
                        item_this_new += item_this[i]
                item_this = item_this_new
                tree_id_1 = tree.insert(tree_id_0, tree_id_1_count, item_this + "#" + str(tree_id_all_count), text=item_this, value=str(tree_id_all_count))
                tree_id_all_count += 1
                tree_id_1_count += 1
            tree_id_0_count += 1
        #print(tree.get_children())

    elif len(file_name) == 0:
        if len(input_file_name) == 0:
            file_name_str.set(file_name_head + "请选择文件！")
        tkinter.messagebox.showwarning("警告","请选择文件！")
    else:
        if len(input_file_name) == 0:
            file_name_str.set(file_name_head + "请一次只选择一个文件！")
        tkinter.messagebox.showwarning("警告","请一次只选择一个文件！")

def tran_save():
    global deck_name
    global t1
    global deck_author
    global t2
    global deck_version
    global t3
    global deck_command
    global deck_desc
    global t4
    global deck_includes
    global t5
    global deck_info
    global deck_default
    global t6
    global input_file_name
    global output_file_name
    #file_name = tkinter.filedialog.asksaveasfilename(initialdir = "./test")
    if len(input_file_name) != 0:
        file_path = tkinter.filedialog.askdirectory(title="选择保存路径")
        if len(file_path) != 0:
            #print(file_path)
            deck_name = t1.get()
            deck_author = t2.get()
            deck_version = t3.get()
            deck_command = t1.get()
            deck_desc = t4.get()
            deck_includes = t5.get().split(",")
            deck_default = t6.get()
            output_file_name = file_path + "/" + deck_name
            #print(deck_includes)
            json2yaml_work()
            tkinter.messagebox.showinfo("完成","已保存到" + output_file_name)
        else:
            tkinter.messagebox.showwarning("警告", "请选择保存路径！")
    else:
        tkinter.messagebox.showwarning("警告", "请先选择要转换的Json文件！")

def show_info():
    tkinter.messagebox.showinfo("Json2Yaml By BenzenPenxil","Json2Yaml基于Python\n作者：仑质(BenzenPenxil)\n版本：" + j2y_version + "\n有问题请联系QQ：137334701")

if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Json2Yaml By BenzenPenxil")
    root.geometry("560x624")
    #root.minsize(560, 632)
    #root.maxsize(560, 632)
    root.resizable(width=False, height=False)

    file_name_head = "Json文件路径："
    file_name_str = tkinter.StringVar()
    file_name_str.set(file_name_head + "请选择文件！")
    L1 = tkinter.Label(root, textvariable = file_name_str)
    L1.place(x=0, y=0, width=500,height=32)

    EtL1 = tkinter.Label(root, text = "名称/命令")
    EtL1.place(x=0, y=432, width=60,height=32)
    t1 = tkinter.StringVar()
    t1.set("名称与命令")
    Et1 = tkinter.Entry(root, textvariable=t1)
    Et1.place(x=60, y=432, width=468, height=32)

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
    Et6.place(x=60, y=592, width=440, height=32)

    Btn1 = tkinter.Button(root, text = "选择文件", command = select_file)
    Btn1.place(x=500, y=0, width=60, height=32)
    Btn2 = tkinter.Button(root, text="开始转换", command = tran_save)
    Btn2.place(x=500, y=592, width=60, height=32)
    Btn3 = tkinter.Button(root, text="i", command = show_info)
    Btn3.place(x=528, y=432, width=32, height=32)


    #测试用
    #t1.set(deck_name)
    #t2.set(deck_author)
    #t3.set(deck_version)
    #t4.set(deck_desc)
    #t5.set(",".join(deck_includes))
    #t6.set(deck_default)


    tree = ttk.Treeview(root)
    tree.place(x=0,y=32,width=560,height=400)
    root.mainloop()
    #json2yaml_work()

