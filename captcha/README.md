# PKUElectiveCaptcha

elective.pku.edu.cn 补选验证码识别


### 封装
为了方便第三方项目使用这个超赞的验证码识别，我将这个识别系统模块化，并重新设计了API。
使用示范：
```
from captcha import recognize_captcha

img_bytes = get_captcha_img()
result = recognize_captcha(img_bytes)
```
