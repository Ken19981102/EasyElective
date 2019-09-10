# EasyElective: 简单易懂的北京大学选课工具

## 快速入门
如果你只是想使用这个工具，请按照下面的步骤进行：
  1. 安装 [python3](https://www.python.org/) ，注意在运行安装程序时要勾选“将python添加到PATH”。
  2. 下载这个 repo 至本地。点击右上角的`Clone or download`即可下载。解压到你喜欢的地方。
  3. 在命令行进入项目根目录（按住 shift 右键单击项目文件夹，点击“在此处打开PowerShell窗口”），输入`pip install -r requirements.txt`安装相应的依赖。如果 PowerShell 提示找不到　pip　，你可能是安装 python 的时候忘记勾选“添加到PATH”了。
  4. 用文本编辑器（比如记事本）修改 config.yaml 填入你的学号和密码。用 Excel 修改 targets.csv 填入你想选的课程。
  5. 在命令行运行 python easyelective.py 运行程序。程序每10秒刷新一次课程列表，并在屏幕上简要地显示日记。

## 开发入门
说是“简单易懂的选课工具”，不仅仅是用起来方便，阅读和修改也应该如此。这个项目的所有代码都在 easyelective.py 一个文件中，目前总计约300行代码。GitHub上另有一个[选课工具](https://github.com/zhongxinghong/PKUAutoElective)，虽然也很好用，但整个 repo 有几千行代码，并运用了许多面向对象的技巧，给阅读增添了一些困难。

我希望通过这个简化版的选课工具，鼓励大家阅读和改进现有的代码。毕竟，你还要把自己选课的命运托付给这些代码呢 XD
