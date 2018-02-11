#!/usr/bin/env python3
#coding=utf-8

# -------------------------------------------------------------------------------
# Filename:    RLUpdateProfile.py
# Revision:    1.0
# Date:        2017/05/27
# Author:      houfeng
# Description: 自动更新证书过期时间
# -------------------------------------------------------------------------------


'''
采用selenium登录apple developer center 做更新证书操作
需要安装 phantomjs , selenium,keyring
 npm install -g cnpm --registry=https://registry.npm.taobao.org
 cnpm install -g phantomjs
 pip3 install  selenium
 pip3 install  keyring
'''


from selenium.webdriver.phantomjs.webdriver import WebDriver as PhantomJS
from selenium.webdriver.support.ui import WebDriverWait
import time
import urllib
import urllib.parse
import urllib.request
import requests
import keyring
import shutil
#from docopt import docopt
import  os
import time,datetime
import codecs
import plistlib
import sys

RL_Temp_Dir = './rlupdateprofiletmp/'
class RLSingleton(type):
    _instances = {}

    def __call__(cls,*args,**kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(RLSingleton,cls).__call__(*args,**kwargs)
        return cls._instances[cls]

class RLDate(object):
    MonthJanuary   = "Jan"
    MonthFebruary  = "Feb"
    MonthMarch     = "Mar"
    MonthApril     = "Apr"
    MonthMay        = "May"
    MonthJune       = "Jun"
    MonthJuly       = "Jul"
    MonthAugust    = "Aug"
    MonthSeptember = "Sep"
    MonthOctober   = "Oct"
    MonthNovember  = "Nov"
    MonthDecember  = "Dec"
    MonthsList = [MonthJanuary, MonthFebruary, MonthMarch, MonthApril, MonthMay, MonthJune, MonthJuly, MonthAugust, MonthSeptember, MonthOctober, MonthNovember, MonthDecember]

    def __init__(self,month=0,day=0,year=0):
        super(RLDate,self).__init__()
        self.month = month
        self.day   = day
        self.year  = year


class RLError(object):
    RLCodeDisableCertificateType = -1
    RLCodeInvalidAppID = - 2
    RLCodeInvalidCertificateExpirationDate = -3
    RLCodeLoginError = -4
    RLCodeNoLoginCredentials = -5

    def __init__(self,code,message):
        super(RLError,self).__init__()
        self.code = code
        self.message = message


class RLDriver(PhantomJS):
    __metaclass__ = RLSingleton
    def __init__(self):
        super(RLDriver,self).__init__()


class RLProvisioner(object):
    ProfileTypeDevelopment = 0
    ProfileTypeAppStore = 1
    ProfileTypeAdHoc = 2

    def __init__(self):
        super(RLProvisioner,self).__init__()

    def generate_development_profile(self, app_id, profile_name, profile_path):
        return self.generate_provisioning_profile(RLProvisioner.ProfileTypeDevelopment, app_id, profile_name, profile_path)

    def generate_app_store_profile(self, app_id, profile_name, profile_path, expiration_date=None):
        return self.generate_provisioning_profile(RLProvisioner.ProfileTypeAppStore, app_id, profile_name, profile_path, date=expiration_date)

    def generate_adhoc_profile(self, app_id, profile_name, profile_path, expiration_date=None):
        return self.generate_provisioning_profile(RLProvisioner.ProfileTypeAdHoc, app_id, profile_name, profile_path, date=expiration_date)

     #以后完善
    def generate_provisioning_profile(self,profile_type,app_id,profile_name,profile_path,date=None):
        print("Generating provisioning profile...")
        self.pick_profile_type(profile_type)
        self.select_app_id(app_id)
        if profile_type == RLProvisioner.ProfileTypeDevelopment:
            self.pick_development_signing_certificate()
        else:
            self.pick_distribution_signing_certificate(date)
        if profile_type == RLProvisioner.ProfileTypeDevelopment or profile_type == RLProvisioner.ProfileTypeAdHoc:
            self.pick_provisioned_devices()
        self.enter_profile_name(profile_name)
        return self.download_provisioning_profile(profile_path)

     #以后完善
    def pick_profile_type(self,profile_type):
        print("Picking profile type...")
        driver.get("https://developer.apple.com/account/ios/profile/profileCreate.action")
        print("打开网页中...")
        print(driver.title)
        print(driver.page_source)

        button_id = ""
        if profile_type == RLProvisioner.ProfileTypeDevelopment:
            button_id = "type-development"
        elif profile_type == RLProvisioner.ProfileTypeAppStore:
            button_id = "type-production"
        elif profile_type == RLProvisioner.ProfileTypeAdHoc:
            button_id = "type-adhoc"
        radio_button = driver.find_element_by_id(button_id)

        radio_button.click()

        submit_button_element = driver.find_element_by_class_name("submit")
        submit_button_element.click()
     #以后完善
    def select_app_id(self,app_id):
        print("Selecting app ID...")

        time.sleep(0.2)

        wait = WebDriverWait(driver,20)
        wait.until(lambda driver:driver.find_element_by_name("appIdId"))

        select_app_id_dropdown = driver.find_element_by_name("appIdId")
        options_list = select_app_id_dropdown.find_elements_by_xpath("./*")
        selected_option = None
        for option in options_list:
            if app_id in option.text:
                selected_option = option
                break
        if type(selected_option) != type(select_app_id_dropdown):
            raise Exception(RLError.RLCodeInvalidAppID,"The app ID provided (" + app_id + ") could not be found.")

        selected_option.click()
        continue_button_element = driver.find_element_by_css_selector(".button.small.blue.right.submit")
        continue_button_element.click()
     #以后完善
    def pick_development_signing_certificate(self):
        print("Picking development certificate...")
        time.sleep(0.2)
        select_all_column = driver.find_element_by_css_selector('.selectAll')
        select_all_checkbox = select_all_column.find_element_by_xpath('./input')
        select_all_checkbox.click()
        continue_button_element = driver.find_element_by_css_selector(".button.small.blue.right.submit")
        continue_button_element.click()
     #以后完善
    def pick_distribution_signing_certificate(self, date):
        print("Picking distribution certfificate...")
        time.sleep(0.2)
        certificates_table = driver.find_element_by_css_selector('.form.table.distribution')
        rows_div = certificates_table.find_element_by_class_name("rows")
        available_certificates = rows_div.find_elements_by_xpath("./*")
        radio_button = None
        if date:
            date_string = date.readable_date()
            for i in available_certificates:
                if i.get_attribute("innerHTML") == date_string:
                    current_date_index = available_certificates.index(i)
                    radio_button = available_certificates[current_date_index-1].find_element_by_xpath("./input")
        else:
            radio_button = available_certificates[-1].find_element_by_xpath("./input")

        try:
            radio_button.click()
        except Exception as e:
            raise Exception(RLError(RLError.RLCodeInvalidCertificateExpirationDate,"InvalidCertificateExpirationDate"))

        continue_button_element = driver.find_element_by_css_selector(".button.small.blue.right.submit")
        continue_button_element.click()

    #以后完善
    def pick_provisioned_devices(self):
        print("Selecting provisioned devices...")
        time.sleep(0.2)
        select_all_column = driver.find_element_by_css_selector('.selectAll')
        select_all_checkbox = select_all_column.find_element_by_xpath('./input')
        select_all_checkbox.click()
        continue_button_element = driver.find_element_by_css_selector(".button.small.blue.right.submit")
        continue_button_element.click()
    #以后完善
    def enter_profile_name(self, profile_name):
        print("Naming provisioning profile...")
        time.sleep(0.2)
        profile_name_element = driver.find_element_by_name("provisioningProfileName")
        profile_name_element.send_keys(profile_name)
        continue_button_element = driver.find_element_by_css_selector(".button.small.blue.right.submit")
        continue_button_element.click()


    #根据证书名更新证书过期时间
    def update_provisioning_profile(self,name):
        print("正在打开证书页面...")
        #https://developer.apple.com/account/ios/profile/limited
        #https://developer.apple.com/account/ios/profile/production
        driver.get("https://developer.apple.com/account/ios/profile/production")
        print(driver.current_url)
        print(driver.title)

        time.sleep(5)

        save_screenshot('production.png')

        print("查找证书 %s" % name)

        wait = WebDriverWait(driver,60)
        wait.until(lambda driver:driver.find_elements_by_css_selector("td.ui-ellipsis.bold"))
        tds = driver.find_elements_by_css_selector("td.ui-ellipsis.bold")
        mytd = None
        for td in tds:
            if td.get_attribute("title") == name:
                mytd = td
                break

        if mytd == None:
            print("没有找到证书%" % name)
            return

        print("点击%s证书列表" % name)
        print(mytd)
        save_screenshot('profilelist.png')
        mytd.click()
        time.sleep(0.2)
        save_screenshot('profilelistclick.png')
        print("查找编辑按钮")
        wait = WebDriverWait(driver,30)
        wait.until(lambda driver:driver.find_elements_by_css_selector('a.button.small.edit-button'))
        editBtns = driver.find_elements_by_css_selector('a.button.small.edit-button')
        print(editBtns)
        editBtn = None
        for btn in editBtns:
            print(btn.get_attribute("data-displayid"))
            if btn.get_attribute('data-displayid') != "":
                editBtn = btn
                break
        if editBtn == None:
            print("没有找到编辑按钮,有可能是网络原因,或者网页结构发生变化,请重新更新脚本.")
            return

        print("点击编辑按钮")
        print(editBtn)
        print(editBtn.get_attribute('data-displayid'))
        print(editBtn.get_attribute('href'))
        span = editBtn.find_element_by_tag_name('span')
        print(span.text)
        span.click()


        time.sleep(5)
        print("查找生成证书按钮")
        save_screenshot('submit1.png')
        wait = WebDriverWait(driver,30)
        wait.until(lambda driver:driver.find_element_by_css_selector("a.button.small.blue.right.submit"))
        submitBtn = driver.find_element_by_css_selector("a.button.small.blue.right.submit")




        print("点击生成证书")
        print(submitBtn)
        generate_btn = submitBtn.find_element_by_tag_name('span')
        print(generate_btn.text)

        generate_btn.click()

        time.sleep(2)
        wait = WebDriverWait(driver,30)
        wait.until(lambda driver:driver.find_element_by_css_selector("a.button.small.blue"))
        down_btn = driver.find_element_by_css_selector("a.button.small.blue")
        down_span =  down_btn.find_element_by_tag_name('span')
        down_span.click()
        down_url = down_btn.get_attribute('href')

        print(down_url)
        if down_url != None:
            print("证书生成成功")
            all_cookies = driver.get_cookies()
            print(all_cookies)
            repCookies = {}
            for s in all_cookies:
                repCookies[s['name']]=s['value']
            print(repCookies)
            r = requests.get(down_url,cookies=repCookies)
            profileContent = r.content
            print(profileContent)
            home_directory = os.path.expanduser("~")
            fileName = name.replace('.','_')
            fileName = fileName.replace('/','')
            fileName = fileName.replace(' ','')
            desFileName = fileName
            tmpProfilePath = "./rlupdateprofiletmp/new.mobileprovision"
            desProfilePath =  home_directory+"/Library/MobileDevice/Provisioning\ Profiles/%s.mobileprovision" % desFileName
            if profileContent != None:
                with open(tmpProfilePath,'wb') as fileHande:
                    fileHande.write(profileContent)
                    if os.path.exists(tmpProfilePath):
                        cmd = "security cms -D -i " + tmpProfilePath
                        plistStr = os.popen(cmd).read()
                        wf = open('./rlupdateprofiletmp/new.plist','w')
                        wf.write(plistStr)
                        wf.close()
                        pl = plistlib.readPlist('./rlupdateprofiletmp/new.plist')
                        if pl != None:
                            desFileName = pl['UUID']
                            print(desFileName)
                        desProfilePath =  home_directory+"/Library/MobileDevice/Provisioning\ Profiles/%s.mobileprovision" % desFileName
                        print('move %s to %s' % (tmpProfilePath,desProfilePath))
                        cmd = 'cp ' + tmpProfilePath +' ' + desProfilePath
                        print(cmd)
                        os.system(cmd)
                        #clearOldProfile()
                        cmd = 'mv ' + tmpProfilePath + ' ' + './rlupdateprofiletmp/%s.mobileprovision' % desFileName
                        print(cmd)
                        os.system(cmd)
                        with open(home_directory + "/.ipos_profile_success",'w') as content_file:
                            content_file.write('T')

        else:
            print("证书生成失败")
        save_screenshot('submit2.png')



class RLAuthenticator(object):
    def __init__(self):
        super(RLAuthenticator,self).__init__()

    def sign_in(self,email=None,password=None):
        print("登陆apple开发者中心...")
        if not os.path.exists(RL_Temp_Dir):
            os.mkdir(RL_Temp_Dir)
        if not email or not password:
            raise Exception(RLError(RLError.RLCodeLoginError,"Login err"))
        driver.get("https://developer.apple.com/account/ios/profile/")
        #print("打开网页中...")
        print(driver.title)
        #print(driver.page_source)
        email_element = driver.find_element_by_name("appleId")
        email_element.send_keys(email)

        password_element = driver.find_element_by_name("accountPassword")
        password_element.send_keys(password)
        save_screenshot('login.png')
        wait = WebDriverWait(driver,30)
        wait.until(lambda driver:driver.find_element_by_id("submitButton2"))
        submitBtn = driver.find_element_by_id("submitButton2")
        print(submitBtn)
        driver.implicitly_wait(10)
        submitBtn.click()
        driver.implicitly_wait(10)
        # wait = WebDriverWait(driver,30)
        # wait.until(lambda driver:driver.find_element_by_css_selector("div.tooltip.top-pointer"))

        if len(driver.find_elements_by_class_name("dserror")) > 0:
            print("登陆失败")
            save_screenshot('loginfail.png')
        else:
            print("登陆成功")
            save_screenshot('loginok.png')



class RLProfileManager(object):
    def __init__(self):
        super(RLProfileManager,self).__init__()

        self.authenticator =RLAuthenticator()
        self.provisioner = RLProvisioner()

driver = RLDriver()
manager = RLProfileManager()
global reTryCount
global updateSucceed
reTryCount = 3
updateSucceed = False


g_username = None
g_password = None



def save_login(email,password):
    keyring.set_password("ipos",email,password)
    home_directory = os.path.expanduser("~")
    with open(home_directory+'/.ipos_session',"w+") as content_file:
        content_file.write(email)

def cache_login():
    home_directory = os.path.expanduser("~")
    if not os.path.exists(home_directory + "/.ipos_session"):
        return  None,None

    with open(home_directory + "/.ipos_session", 'r') as content_file:
        content = content_file.read()
        return content,keyring.get_password("ipos",content)

def clear_login():
    print('清除错误的账号密码')
    home_directory = os.path.expanduser("~")
    if os.path.exists(home_directory+'/.ipos_session'):
        os.remove(home_directory+'/.ipos_session')

def login(email,password):
    print(email + "正在")
    manager.authenticator.sign_in(email,password)



def update():
    deleteTmpFiles()
    print("开始更新证书...")
    login(g_username,g_password)
    #manager.provisioner.update_provisioning_profile("rlterm3pushv6")



def reTryUpdate():
    global reTryCount
    global updateSucceed
    if reTryCount > 0 and not updateSucceed:
        update()
        if updateSucceed:
            return
        print('重试 %i' % reTryCount )
        reTryCount = reTryCount - 1
        reTryUpdate()
    else:
        print("程序执行完毕")



def save_screenshot(name):
    try:
        driver.save_screenshot(RL_Temp_Dir+name)
    except:
        print('save_screenshot error')

def deleteTmpFiles():
    print("清除零时文件...")
    os.system("rm -rf %s"%RL_Temp_Dir)

def clearOldProfile():
    home_directory = os.path.expanduser("~")
    print("清空旧证书...")
    if os.path.exists(home_directory+'/Library/MobileDevice/Provisioning Profiles'):
        shutil.rmtree(home_directory+'/Library/MobileDevice/Provisioning Profiles')
        os.mkdir(home_directory+'/Library/MobileDevice/Provisioning Profiles')


def updateProfile():
    date = datetime.datetime.now()
    weekday =  date.weekday()
    weekday = 0 # 暂时写成每天都更新
    if weekday == 0:
        if date.hour > 8 and date.hour < 24:
            #print("今天是星期一,做一次证书更新操作")
            print("今天是%s" % date.strftime("%Y-%m-%d"))
            print("做一次证书更新操作")
            home_directory = os.path.expanduser("~")
            if not os.path.exists(home_directory + "/.ipos_profile"):
                with open(home_directory + "/.ipos_profile", 'w') as content_file:
                    content_file.write('')
            if not os.path.exists(home_directory + "/.ipos_profile_success"):
                with open(home_directory + "/.ipos_profile_success",'w') as content_file:
                    content_file.write('F')

            with open(home_directory + "/.ipos_profile", 'r') as content_file:
                content = content_file.read()
                success = open(home_directory +"/.ipos_profile_success","r").read()
                if content == date.strftime('%Y%m%d') and success == "T":
                    print("今天已经做过一次更新过了")
                else:
                    with open(home_directory+"/.ipos_profile",'w') as write_file:
                        write_file.write(date.strftime('%Y%m%d'))

                    with open(home_directory + "/.ipos_profile_success",'w') as content_file:
                        content_file.write('F')

                    update()
    else:
        #print("今天不是星期一,不做证书更新操作")
        print("不更新证书")


if __name__ == '__main__':
   if len(sys.argv) > 1:
       if sys.argv[1] == 'clear':
           clear_login()

   g_username,g_password = cache_login()
   g_username = 'Dev@repeatlink.co.jp'
   g_password = 'Repeatlink2804'
   if g_username == None or g_password == None :
       print("第一次运行请输入用户名和密码:")
       g_username = input('Apple ID: ')
       g_password  = input('密码: ')
       save_login(g_username,g_password)

   updateProfile()
