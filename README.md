# EasyElective: 简单易懂的北京大学选课工具

## 快速入门
如果你只是想使用这个工具，请按照下面的步骤进行：
  1. 安装[python3](https://www.python.org/)，注意在运行安装程序时要勾选“将python添加到PATH”。
  2. 下载一份这个repo，解压到你喜欢的地方。
  3. 按住shift右键单击项目文件夹，点击“在此处打开PowerShell窗口”。输入 pip install -r requirements.txt 安装相应的依赖。如果PowerShell提示找不到pip，你可能是安装python的时候忘记勾选“添加到PATH”了。
  4. 用文本编辑器（比如记事本）修改config.yaml填入你的学号和密码。用Excel修改targets.csv填入你想选的课程。运行easyelective.py即可。程序每10秒刷新一次课程列表，并在屏幕上简要地显示日记。
