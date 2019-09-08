#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: const.py

import os
import random
from .util import NoInstance, mkdir

__all__ = [

    "Base_Dir",
    "Model_Dir",
    "Cache_Dir",
    "Log_Dir",
    "Captcha_Cache_Dir",

    "Course_UTF8_CSV",
    "Course_GBK_CSV",
    "Config_INI",

    "User_Agent",

    "IAAALinks",
    "ElectiveLinks",

    ]


__base_dir = os.path.dirname(__file__)
__absP = lambda path: os.path.abspath(os.path.join(__base_dir, path))


Base_Dir          = __absP("./")
Model_Dir         = __absP("./model/")
Cache_Dir         = __absP("./cache/")
Log_Dir           = __absP("./log/")
Captcha_Cache_Dir = __absP("./cache/captcha/")

Course_UTF8_CSV   = __absP("../course.utf-8.csv")
Course_GBK_CSV    = __absP("../course.gbk.csv")
Config_INI        = __absP("../config.ini")

# 警惕直接复制的 User-Agent 中可能存在的省略号（通常源自 Firefox 开发者工具），它可能会引发如下错误：
#   File "/usr/lib/python3.6/http/client.py", line 1212, in putheader
#     values[i] = one_value.encode('latin-1')
# UnicodeEncodeError: 'latin-1' codec can't encode character '\u2026' in position 30: ordinal not in range(256)
User_Agent = random.choice([
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.65",
    "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:62.0) Gecko/20100101 Firefox/62.0",
    ])

mkdir(Cache_Dir)
mkdir(Log_Dir)
mkdir(Captcha_Cache_Dir)


class IAAALinks(object, metaclass=NoInstance):
    """
        Host
        OauthHomePage
        OauthLogin
    """
    __Base_URL    = "https://iaaa.pku.edu.cn/iaaa"

    Host          = "iaaa.pku.edu.cn"
    OauthHomePage = __Base_URL + "/oauth.jsp"
    OauthLogin    = __Base_URL + "/oauthlogin.do"


class ElectiveLinks(object, metaclass=NoInstance):
    """
        Host
        SSOLoginRedirect        重定向链接
        SSOLogin                sso登录
        SSOLoginDualDegree      sso登录（双学位）
        Logout                  登出
        HelpController          选课帮助页
        ElectivePlanController  选课计划页
        ElectiveWorkController  选课页
        ShowResults             选课结果页
        SupplyCancel            补退选页
        CourseQueryController   课程查询页
        GetCurriculmByForm      发送查询表单
        addToPlan               添加课程到选课计划
        DeleElecPlanCurriclum   删除选课计划（补退选阶段）
        validate                补退选验证码校验接口
    """
    __Base_URL             = "http://elective.pku.edu.cn/elective2008"
    __Controller_Base_URL  = __Base_URL + "/edu/pku/stu/elective/controller"

    Host                   = "elective.pku.edu.cn"
    SSOLoginRedirect       = "http://elective.pku.edu.cn:80/elective2008/agent4Iaaa.jsp/../ssoLogin.do"
    SSOLogin               = __Base_URL + "/ssoLogin.do"
    SSOLoginDualDegree     = "http://elective.pku.edu.cn:80/elective2008/scnStAthVef.jsp/../ssoLogin.do"
    Logout                 = __Base_URL + "/logout.do"
    HelpController         = __Controller_Base_URL + "/help/HelpController.jpf"
    ElectivePlanController = __Controller_Base_URL + "/electivePlan/ElectivePlanController.jpf"
    ElectiveWorkController = __Controller_Base_URL + "/electiveWork/ElectiveWorkController.jpf"
    ShowResults            = __Controller_Base_URL + "/electiveWork/showResults.do"
    SupplyCancel           = __Controller_Base_URL + "/supplement/SupplyCancel.do"
    SupplyOnly             = __Controller_Base_URL + "/supplement/SupplyOnly.do"
    #CourseQueryController  = __Controller_Base_URL + "/courseQuery/CourseQueryController.jpf"
    #GetCurriculmByForm     = __Controller_Base_URL + "/courseQuery/getCurriculmByForm.do"
    #AddToPlan              = __Controller_Base_URL + "/courseQuery/addToPlan.do"
    #DeleElecPlanCurriclum  = __Controller_Base_URL + "/electivePlan/deleElecPlanCurriclum.do"
    DrawServlet            = __Base_URL + "/DrawServlet"
    Validate               = __Controller_Base_URL + "/supplement/validate.do"
