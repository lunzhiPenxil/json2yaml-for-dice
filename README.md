## Json2Yaml for Dice
网上跑团时进行Roll点判定的解决方案中，当前的主流方案是基于酷Q的骰子机器人，其中实现骰值的主流插件为[塔系核心(By SinaNya)](https://sinanya.com/#/)、[Dice!(By 溯洄)](https://kokona.tech/)、Shiki系(By Shiki)等。    
牌堆功能是各类主流插件中一项可由骰主进行定制的功能，以数据序列化交换格式文件的形式进行编写，其中一部分插件采用了Json格式，而本人所使用的**塔系核心**采用了Yaml格式，因此不同插件的骰主之间进行牌堆内容的交流时出现了数据不互通与重复工作的问题，尽管目前也有Json到Yaml的在线转换器，但往往在一些细节处不尽如人意，转换生成的文件并不能直接被载入使用。    
    
**基于以上情况，本人基于Python实现了一个具有图形交互界面且针对骰子牌堆优化的转换器。**    
    
## 获取工具
请移步[Release页面](https://github.com/lunzhiPenxil/json2yaml-for-dice/releases)。
    
## 更新日志      
	2020/01/17：[+] 增加了右键菜单
	2020/01/17：[+] 增加了操作栏功能
	2020/01/17：[+] 增加了项目主页的入口
	2020/01/17：[+] 增加了进度条
	2020/01/17：[+] 增加了对于emoji的支持
	2020/01/16：[+] 将输入栏的默认信息设置为简单引导
	2020/01/16：[+] 将交互按钮集成至新增的菜单栏
	2020/01/16：[+] 增加了简单的导入文件查错功能
	2020/01/15：[+] 对部分复用代码进行重构
	2020/01/15：[+] 实现进程图标嵌入
	2020/01/14：[+] 实现基本转换功能

 
