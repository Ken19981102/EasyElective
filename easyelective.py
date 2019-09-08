import logging
import yaml
import csv
from collections import namedtuple
from time import sleep

import requests
from requests.exceptions import Timeout

from captcha import recognize_captcha

class EasyElectiveException(Exception):
    """Base exception"""
    pass

class ConnectionError(EasyElectiveException):
    """Network failure, connection timeout, etc"""
    pass

class IllegalOperationError(EasyElectiveException):
    """Not logged in, caught cheating, no such course, etc"""
    session_expired = False

    def __init__(self, session_expired = False):
        self.session_expired = session_expired


# Data structure for a course
Course = namedtuple('Course', ['name', 'classID', 'teacher', 'max_slots', 'used_slots', 'elect_address'])

logger = logging.getLogger(__name__)


def get_iaaa_token(appid, username, password, redir):
    url = 'https://iaaa.pku.edu.cn/iaaa/oauthlogin.do'
    form = dict(appid=appid, userName=username, password=password, randCode='', smsCode='', otpCode='', redirUrl=redir)

    r = requests.post(url, data=form, timeout=2)

    token = r.json()['token']
    logger.info("Got token from IAAA")
    return token


def get_elective_session(username, password):
    sess = requests.Session()

    # Fake referer and user agent
    sess.headers['Referer'] = 'http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/help/HelpController.jpf'
    sess.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'

    # Pass username and password to IAAA, and get IAAA token
    appid = 'syllabus'
    redir = 'http://elective.pku.edu.cn:80/elective2008/agent4Iaaa.jsp/../ssoLogin.do'
    token = get_iaaa_token(appid, username, password, redir)

    # Pass IAAA token to elective.pku.edu.cn, and get elective session
    login_url = 'http://elective.pku.edu.cn/elective2008/ssoLogin.do'
    try:
        sess.get(login_url, params={"token": token}, timeout=2)
        logger.info("Successfully got elective session")
        return sess
    except Timeout as e:
        raise ConnectionError from e


def get_courses(session):
    """Return an list of courses in selection plan"""
    # Pages for course list. Two is enough for now:)
    url1 = 'http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/supplement/SupplyCancel.do'
    url2 = 'http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/supplement/supplement.jsp?netui_pagesize=electableListGrid%3B50&netui_row=electableListGrid%3B50'

    courses = []

    for url in url1, url2:
        try:
            r = session.get(url, timeout=1)
            # Parse HTML
            table = r.html.find('table.datagrid', first=True)
            items = table.find('tr.datagrid-even,tr.datagrid-odd')
        except Exception as e:
            raise IllegalOperationError from e

        for item in items:
            data = item.find('td.datagrid')
            # Parse course info
            name = data[0].text
            classID = int(data[5].text)
            teacher = data[4].text
            maxSlots, usedSlots = (int(s) for s in data[9].text.split('/'))
            electAddr = data[10].absolute_links.pop()
            courses.append(Course(name, classID, teacher, maxSlots, usedSlots, electAddr))
    return courses


def pass_captcha(session):
    """Request captcha from elective and upload the correct answer"""
    # Request a new captcha
    request_captcha_url = 'http://elective.pku.edu.cn/elective2008/DrawServlet'
    img_bytes = session.get(request_captcha_url).content

    # TODO: If we do not receive an image, raise session expired
    pass

    # Recognize the captcha
    result = recognize_captcha(img_bytes)

    # Upload result to elective
    submit_url = 'http://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/supplement/validate.do'
    resp = session.post(submit_url, data={"validCode": result}, timeout=2)

    # If failed, retry
    if resp.json()['valid'] != '2':
        pass_captcha(session)


def elect(session, course):
    """Attempt to elect a course"""
    logger.info("Attempting to elect {course.name}".format(course=course))
    if course.usedSlots < course.maxSlots:
        # Pass a captcha
        pass_captcha(session)

        url = course.elect_address
        try:
            r = session.get(url)
            msg = r.html.find('#msgTips', first=True).text
        except Exception as e:
            raise IllegalOperationError(session_expired=True) from e

        if '成功' in msg:
            logger.info("Successfully elected {}".format(course.name))
        else:
            logger.warning("Failed to elect {}: {}".format(course.name, msg))
            raise IllegalOperationError


def main():
    # Load config
    with open('config.yaml') as config_file:
        config = yaml.load(config_file)
        username = config['studentID']
        password = config['password']

    # Load target courses
    # TODO: restore wildcard course selection
    with open('courses.csv', newline='') as courses_file:
        csv_reader = csv.DictReader(courses_file)
        targets = list(csv_reader)

    # Login into elective
    # TODO: deal with login error
    sess = get_elective_session(username, password)

    # Ignore courses that causes conflicts
    # TODO: clean up "ignored courses"
    ignored_courses = []

    # Check course availability at regular interval
    while targets:
        try:
            courses = get_courses(sess)
            for target in targets:
                # Search courses that correspond to target name and classID
                search_result = [course for course in courses if course.name == target['courseName'] if course.classID == target['classID']]
                # Warn if no course correspond to target
                logger.warning("{} not found in election plan.".format(targets['courseName']))
                targets.remove(target)
                # Filter out ignored courses
                search_result = [course for course in search_result if not any(course.name == ignored.name and course.classID == ignored.classID for ignored in ignored_courses)]

                for course in search_result:
                    if course.usedSlots < course.maxSlots:
                        logger.info(
                            "Discovered a electable course: {course.name}, class {course.classID},"
                            " {course.maxSlots}/{course.usedSlots}".format(course=course))
                        elect(sess, course)
                        targets.remove(target)
        except IllegalOperationError as e:
            if e.session_expired:
                sess = get_elective_session(username, password)
            else:
                # TODO: clarify what happened
                logger.warning("Illegal Operation detected")
        finally:
            # TODO: export sleep interval in config
            sleep(10)
