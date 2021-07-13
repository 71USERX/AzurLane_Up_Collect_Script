import re

# ********************************************************
# 全局变量存放区
# ********************************************************

# 获取搜索结果需要的api
# 当然你也可以把keyword=后面的内容换成其他的。
address = "http://api.bilibili.com/x/web-interface/search/type?keyword=%e7%a2%a7%e8%93%9d%e8%88%aa%e7%ba%bf&search_type=article&category_id=16&page="

# 获取用户昵称需要的api
InfoAddr = "http://api.bilibili.com/x/space/acc/info?mid="

# 用户B站个人主页
UsrPage = "https://space.bilibili.com/"

# 查找uid所用的正则
regeX = re.compile(r'"mid":.\d+,')

# 查找昵称所用的正则
nameRegeX = re.compile(r'"name":"\S+?",')

# 等待时间
waitingTime = 5

# 已查找到的所有uid
uids = []

# 线程临时存放uid的列表
thread_in = []
thread_seq = []
finder_in = []
finder_seq = []
