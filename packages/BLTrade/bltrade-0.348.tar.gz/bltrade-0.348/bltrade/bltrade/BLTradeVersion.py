# BLTrade Version
import subprocess
import configparser



# Git版本提交次数
def GetGitPushCount():
    
    gitpushcount=subprocess.getoutput('git rev-list --count HEAD')
    return gitpushcount

# 获取版本号
def GetDevVersion():
    try:
        BLTradeVersion=GetGitPushCount()
        #BLTradeVersion=subprocess.getoutput('gitx')
        #return f"BLTrade Engine Version: {int(BLTradeVersion)/1000}"
        # 始终保留三位子版本号
        # eg: 1.025
        return f"{format(float(BLTradeVersion)/1000, '.3f')}"
    except ValueError:
        print("Excepted: git命令执行失败!!!")
        BLTradeVersion=287
        #return f"BLTrade Engine Version: {int(BLTradeVersion)/1000}"
        return f"{int(BLTradeVersion)/1000}"
    
def GetVersion():
        
        file = "bltrade/config/version.ini"

        # 创建配置文件对象
        conf=configparser.ConfigParser()

        # 读取文件
        conf.read(file, encoding='utf-8')

        # 获取所有section
        #sections = conf.sections()
        # ['url', 'email']


        # 获取特定section
        #items = con.items('url') 	# 返回结果为元组
        # [('baidu','http://www.baidu.com'),('port', '80')] 	# 数字也默认读取为字符串

        # 可以通过dict方法转换为字典
        #items = dict(items)

        # 获取特定section
        #items = conf.items('version') 	# 返回结果为元组
        #print(items)

        version=conf.get('version','bltradeversion')
        print(version)

        BLTradeVersion=version
        #return f"BLTrade Engine Version: {int(BLTradeVersion)/1000}"
        #return f"{int(BLTradeVersion)/1000}"
        return BLTradeVersion


        
    

#print(GetVersion())