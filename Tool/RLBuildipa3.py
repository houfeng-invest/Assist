#!/usr/bin/python3
#coding=utf-8

# -------------------------------------------------------------------------------
# Filename:    RLBuildipa3.py
# Revision:    3.0
# Date:        2017/01/11
# Author:      houfeng
# Description: 根据客户配置生成ipa文件
# -------------------------------------------------------------------------------

import os
import argparse
import sys
import plistlib
from collections import deque
from datetime import datetime
import smtplib
import email.mime.multipart
import email.mime.text
import getpass
import functools
from subprocess import Popen, PIPE

def log(text):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args,**kw):
			print('%s %s():' % (text,func.__name__))
			return func(*args,**kw)
		return wrapper
	return decorator




g_APPNAME = {
"UNN":"RLASP6_UNNEAU",
"KF":"RLASP6_TEST",
"CJ":"RLASP6_CJ",
"KKB":"RLASP6_KKB",
"MH":"RLASP6_MH",
"MHBS":"RLASP6_MHBS",
"HGM":"RLASP6_HGM",
"MS":"RLASP6_MS",
"CD":"RLASP6_MH",
"JPDell":"RLASP6_MH",
"JPHP":"RLASP6_MH",
"YC":"RLASP6_YSCARE",
"MUSE":"RLASP6_MUSE",
"TR":"RLASP4_TRICIA",
"AQUA":"RLASP6_AQUA",
"BLX":"RLASP6_BELLEX",
"ZENTOUI":"RLASP6_ZENTOUI",
"AMI":"RLASP6_ZENTOUI",
"YOTUBA":"RLASP6_ZENTOUI",
"KUJIRA":"RLASP6_ZENTOUI",
"IRUKA":"RLASP6_ZENTOUI",
"RLDEV":"RLASP6_DEV",
"YAMADA":"RLASP5_YAMADA",
"LANDMARK":"RLASP6_LANDMARK",
"AUTOIPOS":"RLASP6_AUTOIPOS",
"REZEPT":"RLASP6_REZEPT",
"REZEPT2":"RLASP6_REZEPT2",
"SAKURAR":"RLASP6_SAKURAR",
"RF":"RLASP6_RAYFIELD"
}

g_PRINTER_IP = '192.168.1.198'
g_DEBUG = False
g_FROMMAIL = 'libin@repeatlink.cn'
g_FROMMAILPWD = ''
# g_FROMMAIL = 'iposrl@repeatlink.cn'
# g_FROMMAILPWD = 'Iposrl123456'
g_TOMAIL = 'testers@repeatlink.cn'
g_CCMAIL = 'ipos@repeatlink.cn'
g_CODE_SIGN_IDENTITY = 'iPhone Distribution: REPEAT LINK, K.K.'
g_DYSM_SERVER = '192.168.1.187'
g_DYSM_PATH = '/var/www/html/ipos/IPOS_DYSM/'
class Config:
	'''发布相关配置'''
	def __init__(self):
		self.appName = 'MS'
		self.appNames = []
		self.iposConfigPath = './Config'
		self.iposConfigPathInProject = '../pos/Config/'
		self.buildInfoPath = './Config/buildinfo.plist'
		self.buildPath = './build/'
		self.xcodeBuildOptionsPath = './build/options.plist'
		self.serverAddr = '192.168.1.187'
		self.oneAPMToken = 'F8A1545D9FBF79AC1EBC8828D22CE54F21'
		self.sshName = 'repeatlink'
		self.sshPasswd = 'repeatlink'
		self.iposSuperPathInServer = '/var/www/html/ipos/'
		self.teamID = '272N4285KM'
		self.svnNo = '0'
		self.buildTime = datetime.now().strftime('%Y%m%d%H%M%S')
		self.shouldUpdateSVNNO = None
		self.isPublish = False
		self.iposVer = '0.0'
		self.ipaFilePath = ''
		self.ipaURL = ''
		self.configOnly = False
		self.updateProfile = True


	def getAllAppnames(self):
		print ("\n")
		self.appNames = []
		for f in os.listdir(self.iposConfigPath):
			if f.find('config_') != -1 and f.endswith('xml'):
				s = f.find('_') + 1
				e = f.find('.')
				appName = f[s:e]
				if appName != 'template':
					self.appNames.append(appName)



	def checkAppname(self):
		self.getAllAppnames()
		if self.appName == 'all':
			return True
		elif self.appName in self.appNames:
			return True
		else:
			return False


	def clearTempData(self):
		if os.path.exists(self.buildPath):
			os.system("rm -rf %s" % self.buildPath)
		os.system("mkdir %s" % self.buildPath)


	def createBuildInfoPlist(self):
		wf = open(self.buildInfoPath,'w')
		timeStamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		svnNo =  GetSVNInfoCommand().execute().strip()
		self.svnNo = svnNo
		content = """
		<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>build_timestamp</key>
	<string>%s</string>
	<key>oneapm_token</key>
	<string>%s</string>
	<key>svn_revision</key>
	<string>%s</string>
	<key>client</key>
	<string>%s</string>
</dict>
</plist>
		""" % (timeStamp,self.oneAPMToken,svnNo,self.appName)
		print(content)
		wf.write(content)
		wf.close()



	def createXcodeBuildOptionPlist(self):
		optionPlist = '''
		<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>compileBitcode</key>
    <true/>
    <key>method</key>
    <string>enterprise</string>
    <key>provisioningProfiles</key>
    <dict>
    <key>com.repeatlink.rlterm3push.v6</key>
    <string>rlterm3pushv6</string>
    </dict>
    <key>signingCertificate</key>
    <string>iPhone Distribution</string>
    <key>signingStyle</key>
    <string>automatic</string>
    <key>stripSwiftSymbols</key>
    <true/>
    <key>teamID</key>
    <string>%s</string>
    <key>thinning</key>
    <string>&lt;none&gt;</string>
</dict>
</plist>
		''' % (self.teamID)
		print (optionPlist)
		wf = open(self.xcodeBuildOptionsPath,'w')
		wf.write(optionPlist)
		wf.close()


	def createIposConfig(self):
		command = "cd %s;cp -f config_%s.xml config.xml" % (self.iposConfigPath, self.appName)
		print(command)
		os.system(command)
	def modifyConfigForTest(self):
		print ('修改配置文件为本地测试环境')
		config_path = '%s/config.xml' % self.iposConfigPath
		print (config_path)
		f = open(config_path,'r')
		lines = f.readlines()
		contents = ''
		for line in lines:
			if line.find('<server>') > 0:
				mline = "\t\t<server>%s</server>\n" % self.serverAddr
				contents += mline
				print(mline)
			elif line.find("domain") > 0:
				mline = "\t\t<domain>https://%s</domain>\n" % self.serverAddr
				contents += mline
				print(mline)
			elif line.find("<app_name>") > 0:
				appName =  g_APPNAME[self.appName]
				mline = "\t\t<app_name>%s</app_name>\n" % appName
				contents += mline
				print (mline)
			elif line.find("<ipaddress>") > 0:
				mline = "\t\t<ipaddress>%s</ipaddress>\n" % g_PRINTER_IP
				contents += mline
				print(mline)
			else:
				contents += line

		f.close()

		if not g_DEBUG:
			with open(config_path,'w') as wf:
				wf.write(contents)
				wf.close()


	def encryptIposConfigFile(self):
		command = "cd %s;./RLAES2;cp -f pconfig.xml %s/pconfig.xml;cp -f buildinfo.plist %s/buildinfo.plist" % (self.iposConfigPath, self.iposConfigPathInProject, self.iposConfigPathInProject)
		if not g_DEBUG:
			os.system(command)

	def checkBuildCompleted(self):
		print ("检查发布成功与否...")
		#curPath = os.getcwd()
		#ipaPath = curPath + self.ipaFilePath[1:]
		#print (ipaPath)
		#print (os.path.exists(ipaPath))
		#if os.path.exists(ipaPath):
		#	return True
		#return False
		for f in os.listdir(self.buildPath):
			if f.find('.ipa') != -1 :
				return True
			print (f)

		return False







class PublishConfig(Config):
	def __init__(self):
		super().__init__()
		self.serverAddr = 'hp.repeatlink.co.jp'
		self.oneAPMToken = "0E2FB1DA4F9514D9C717FEEED6214DE421"
		self.sshName = 'repeatlink'
		self.sshPasswd = ''
		self.iposSuperPathInServer = '/var/www/html/ipos/'
		self.isPublish = True
		print('初始化发布正式环境配置')


#context
class Context:
	'Execute context'
	def __init__(self):
		pass
	def handle(self,command):
		pass


class TerminalContext(Context):
	def __init__(self):
		super().__init__()

	def handle(self,command):
		super().handle(command)
		if not g_DEBUG:
			os.system(command.command)

class SystemPoppenContext(Context):
	def __init__(self):
		super().__init__()

	def handle(self,command):
		super().handle(command)
		os_stream = None
		if not g_DEBUG:
			os_stream = os.popen(command.command)
		return os_stream




#end context


#command
class Command:
	def __init__(self,command = ''):
		self.context = TerminalContext()
		self.command = command
		self.description = ''

	def setContext(context):
		self.context = context

	def execute(self):
		print (self.description)
		print ('执行命令: %s' % self.command)
		self.context.handle(self)


class CommandGroup(Command):
	def __init__(self,g=[]):
		self.g = g

	def execute(self):
		for com in self.g:
			com.execute()

#end command

class GetSVNInfoCommand(Command):

	def __init__(self,command=''):
		self.context = SystemPoppenContext()
		self.command = "svn info . | grep \"Last Changed Rev\""
		self.description = '获取SVN号'
	def execute(self):
		rev = '0'
		os_stream = self.context.handle(self)
		if os_stream == None:
			return rev

		rev_str = os_stream.read()
		if len(rev_str) > 1 and rev_str.find(":") != -1:
			tokens = rev_str.split(":")
			rev = tokens[1]

		print('获取SVN号%s' % rev)
		return rev


class GetIpaInfoCommand(Command):
	def __init__(self):
		pass
	def execute(self):
		if g_DEBUG:
			return None
		pl = plistlib.readPlist(self.command)
		print (pl)
		return pl


class CreateIpaPlistCommand(Command):
	def __init__(self):
		self.plistPath = "./"
	def execute(self):
		print("开始执行获取过期时间命令")
		#plistStr = Popen(self.command, shell=True,stdout=PIPE, stderr=PIPE).stdout.readlines()
		plistStr = os.popen(self.command).read()
		print(plistStr)
		wf = open('%sipaInfo.plist' % self.plistPath,'w')
		wf.write(plistStr)
		wf.close()
		pl = plistlib.readPlist('%sipaInfo.plist' % self.plistPath)
		return pl


class SendMailCommand(Command):
	def __init__(self):
		self.appName = ''
		self.svnNo = ''
		self.iposVer = ''
		self.ipaFilePath = ''
		self.ipaURL = ''
		pass
	def execute(self):
		print('发送邮件...')
		msg = email.mime.multipart.MIMEMultipart()
		msg['from']= g_FROMMAIL
		msg['to']= g_TOMAIL
		msg['cc']= g_CCMAIL
		msg['subject']= '%s版 iPOS 发布' % self.appName
		content = '''
			%s版iPos v%s svn %s 发布成功! \n %s
		''' %(self.appName,self.iposVer,self.svnNo,self.ipaURL)
		txt = email.mime.text.MIMEText(content)
		msg.attach(txt)

		smtp = smtplib
		smtp=smtplib.SMTP()
		smtp.connect('smtp.qq.com','25')
		smtp.login(g_FROMMAIL,g_FROMMAILPWD)
		smtp.sendmail(g_FROMMAIL,[g_TOMAIL,g_CCMAIL],str(msg))
		smtp.quit()



#todo

class PushIpaToLocalServerCommand(Command):
	def __init(self,com):
		super().__init__(com)
		pass


class PushIpaToHPServerCommand(Command):
	def __init(self,com):
		super().__init__(com)
		pass



class BuildPipe:
	def __init__(self,config=None):
		self.config = config
		self.queue = deque()
		self.isPublish = False
		self.isAutoTest = False

	def addCommand(self,command):
		self.queue.append(command)

	def execute(self):
		print("准备向 %s 发布iPos" % self.config.serverAddr)
		command =  'svn up'
		if self.config.shouldUpdateSVNNO :
			command = 'svn up -r%s' % self.config.shouldUpdateSVNNO

		svnUpCom = Command(command)
		svnUpCom.execute()

		self.config.clearTempData()
		self.config.createBuildInfoPlist()
		self.config.createXcodeBuildOptionPlist()
		self.config.createIposConfig()


		if not self.config.isPublish:
			self.config.modifyConfigForTest()

		self.config.encryptIposConfigFile()

		if self.config.configOnly :
			return

		#command = "xcodebuild -workspace rlterm3.xcworkspace -scheme rlterm3 archive -archivePath %srlterm3.xcarchive CODE_SIGN_IDENTITY=%s "%(self.config.buildPath,'"%s"'%g_CODE_SIGN_IDENTITY)
		command = "xcodebuild DEBUG_INFORMATION_FORMAT='dwarf-with-dsym' DWARF_DSYM_FOLDER_PATH='%s' -workspace rlterm3.xcworkspace -scheme rlterm3 archive -archivePath %srlterm3.xcarchive "%(self.config.buildPath,self.config.buildPath)
		buildXcarchive = Command(command)
		print(buildXcarchive.command)
		buildXcarchive.description = '生成.xcarchive文件'
		buildXcarchive.execute()


		command = "xcodebuild  -exportArchive  -archivePath %srlterm3.xcarchive    -exportPath %s    -exportOptionsPlist %s  " % (self.config.buildPath,self.config.buildPath,self.config.xcodeBuildOptionsPath)
		createIpaCom = Command(command)
		createIpaCom.description = '生成.ipa文件'
		createIpaCom.execute()

		getIpaInfoCom = GetIpaInfoCommand()
		getIpaInfoCom.command = '%srlterm3.xcarchive/Info.plist' % self.config.buildPath
		ipaInfo = getIpaInfoCom.execute()

		createIpaPlistCom = CreateIpaPlistCommand()
		createIpaPlistCom.plistPath = self.config.buildPath
		createIpaPlistCom.command = "security cms -D -i %srlterm3.xcarchive/Products/Applications/rlterm3.app/embedded.mobileprovision" % self.config.buildPath
		print(createIpaPlistCom.command)
		ipaPlistInfo =  createIpaPlistCom.execute()
		expDate = ipaPlistInfo['ExpirationDate']
		print('ipa过期时间为:' + str(expDate))
		expDateStr =  expDate.strftime('%Y%m%d')
		print(expDateStr)


		rlterm3_ver = '0.0'
		if ipaInfo:
			rlterm3_ver = ipaInfo['ApplicationProperties']['CFBundleVersion']
		print(rlterm3_ver)
		self.config.iposVer = rlterm3_ver


		ipaNamePath =  "%srlterm3_%s_Release_r%s_%s_%s_%s.ipa" % (self.config.buildPath,rlterm3_ver,self.config.svnNo,self.config.appName,self.config.buildTime,expDateStr)
		self.config.ipaFilePath = ipaNamePath
		print(self.config.ipaFilePath)
		command = "mv %srlterm3.ipa %s" % (self.config.buildPath,ipaNamePath)
		modifyIpaNameCom = Command(command)
		modifyIpaNameCom.execute()

		makeDirToServer = Command('')
		todaytime = datetime.now().strftime('%Y%m%d')
		if self.config.isPublish:
			makeDirToServer.command = "ssh %s@%s sh -x /var/www/ipospublish.sh %s %s %s %s" % (self.config.sshName, self.config.serverAddr,self.config.appName.lower(),rlterm3_ver,self.config.svnNo,todaytime)
		else:
			makeDirToServer.command = "ssh %s@%s sh -x /var/www/apps/scripts/iposindex.sh %s %s %s %s" % (self.config.sshName, self.config.serverAddr,self.config.appName,rlterm3_ver,self.config.svnNo,todaytime)

		pushIpaToServer = Command('')
		if self.config.isPublish:
			pushIpaToServer.command = "export RSYNC_PROXY=192.168.1.187:8118;rsync --password-file=/Users/jianghong/ipos.pas %srlterm3_*.ipa rsync://repeatlink@%s/ipos/%s/v%sr%s/rlterm3.ipa" % (self.config.buildPath, self.config.serverAddr,self.config.appName.lower(),rlterm3_ver,self.config.svnNo)
            #pushIpaToServer.command = "scp %srlterm3_*.ipa %s@%s:%s%s/v%sr%s/rlterm3.ipa" % (self.config.buildPath, self.config.sshName, self.config.serverAddr, self.config.iposSuperPathInServer,self.config.appName.lower(),rlterm3_ver,self.config.svnNo)
		else:
			pushIpaToServer.command = "scp %srlterm3_*.ipa %s@%s:%s%s/v%s_r%s_%s/rlterm3.ipa" % (self.config.buildPath, self.config.sshName, self.config.serverAddr, self.config.iposSuperPathInServer,self.config.appName,rlterm3_ver,self.config.svnNo,todaytime)

		pushdSYMToServer = Command('')
		if self.config.isPublish:
			pushdSYMToServer.command = "scp -r %srlterm3.app.dSYM %s@%s:%srlterm3_%s_Release_r%s_%s_%s.app.dSYM" % (self.config.buildPath,self.config.sshName, g_DYSM_SERVER, g_DYSM_PATH,rlterm3_ver,self.config.svnNo,self.config.appName,self.config.buildTime)
		else:
			pushdSYMToServer.command = "scp -r %srlterm3.app.dSYM %s@%s:%s%s/v%s_r%s_%s/rlterm3.app.dSYM" % (self.config.buildPath, self.config.sshName, self.config.serverAddr, self.config.iposSuperPathInServer,self.config.appName,rlterm3_ver,self.config.svnNo,todaytime)


		iposAppName = self.config.appName
		if self.config.isPublish:
			iposAppName = self.config.appName.lower()
			self.config.ipaURL = 'https://%s/ipos/%s/v%sr%s/index.html\n ' % (self.config.serverAddr,iposAppName,rlterm3_ver,self.config.svnNo)
		else:
			self.config.ipaURL = 'https://%s/ipos/%s/v%s_r%s_%s/\n ' % (self.config.serverAddr,iposAppName,rlterm3_ver,self.config.svnNo,todaytime)


		sendToServer = CommandGroup([makeDirToServer,pushIpaToServer,pushdSYMToServer])
		sendToServer.execute()

		while(len(self.queue) > 0):
			command = self.queue.popleft()
			command.execute()




if  __name__ == '__main__':

	if sys.version_info < (3,0):
		print('RLBuildipa3.py 必须使用 python3')
		sys.exit(1)

	parser = argparse.ArgumentParser()
	parser.add_argument('app',help='输入应用名缩写,例如 AQUA, all 表示批量发布')
	parser.add_argument('-p',help='发布模式 (T,F)。默认为 F (False)',default='F')
	parser.add_argument('-r',help='指定版本号 -r 2014',default=None)
	parser.add_argument('-teamid',help='指定证书 RL:272N4285KM , KF:3RB24HNLEQ -r 2014',default='272N4285KM')
	parser.add_argument('-debug',help='debug模式 只是显示命令 不执行,(T,F)',default='F')
	parser.add_argument('-m',help='是否发送邮件,(T,F)',default='F')
	parser.add_argument('-cs',help='指定发布证书',default='iPhone Distribution: REPEAT LINK, K.K.')
	parser.add_argument('-configOnly',help='是否只用于修改配置，(T,F)',default='F')
	parser.add_argument('-updateProfile',help='更新证书有效期,(T,F)',default='T')
	args = parser.parse_args()

	config = None
	if args.p == 'T' :
		config = PublishConfig()
	else:
		config = Config()

	config.appName = args.app
	if args.teamid :
		config.teamID = args.teamid

	if args.r :
		config.shouldUpdateSVNNO = args.r

	if args.debug == 'T':
		g_DEBUG = True
	else:
		g_DEBUG = False

	if args.configOnly == 'T':
		config.configOnly = True
	else:
		config.configOnly = False
	#改为发送HP时候才做证书更新
	if args.updateProfile == 'T':
		config.updateProfile = True
	else:
		config.updateProfile = False

	if args.p == 'T' :
		config.updateProfile = True
	else:
		config.updateProfile = False

	if args.cs :
		g_CODE_SIGN_IDENTITY = args.cs

	if args.app == 'all':
		config.getAllAppnames()
		print (config.appNames)
		count = 1
		for name in config.appNames:
			config.appName = name
			pipe = BuildPipe(config)
			pipe.execute()
			print ('%d %s版本ipa 编译完成'% (count,name))
			count += 1
	else:
		if  not config.checkAppname():
			print('请输入正确的app缩写名!')
		else:
			if config.updateProfile and not config.configOnly :
				os.system('python3 RLUpdateProfile.py')

			pipe = BuildPipe(config)
			lsCom = Command("ls -la %s"%config.buildPath)
			lsCom.description = '显示ipa文件'
			pipe.addCommand(lsCom)


			pipe.execute()


			if args.m == 'T' :
				if  config.checkBuildCompleted() or g_DEBUG:
					if g_FROMMAILPWD == '' or g_FROMMAILPWD == None:
						#g_FROMMAILPWD = input("请输入发送邮箱 %s 的密码:\n" % g_FROMMAIL)
						g_FROMMAILPWD = getpass.getpass("请输入发送邮箱 %s 的密码:\n " % g_FROMMAIL)
					sendMailCom = SendMailCommand()
					sendMailCom.appName = config.appName
					sendMailCom.svnNo = config.svnNo
					sendMailCom.iposVer = config.iposVer
					sendMailCom.ipaFilePath = config.ipaFilePath
					sendMailCom.ipaURL = config.ipaURL
					sendMailCom.execute()
				else:
					print('没有生成.ipa文件发布失败。')
