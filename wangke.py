from selenium import webdriver  
import time

browser = webdriver.Chrome(executable_path=r"...\chromedriver.exe")  # 双引号内添加浏览器驱动的地址

url = "http://passport2.chaoxing.com/login?fid=183&refer=http://i.mooc.chaoxing.com" #这里改成自己学校的学习通登录地址
browser.get(url)

def input_usename_and_password():
    inp_1="..."#这里输入账号
    inp_2="..."#这里输入密码
    inp_3 = input("请输入验证码:")#验证码的自动识别很麻烦，这里为了简化就直接手动输入了
    username = browser.find_element_by_id("unameId")
    password = browser.find_element_by_id("passwordId")
    verycode = browser.find_element_by_id("numcode")
    username.send_keys(inp_1)
    password.send_keys(inp_2)
    verycode.send_keys(inp_3)
    sbm = browser.find_element_by_class_name("zl_btn_right")
    time.sleep(1)
    sbm.click()


# 一级页面跳转,进入首页，开始选择课程
def level_1st():
    browser.switch_to.frame("frame_content")
    # 进入首页，开始选择课程
    time.sleep(1)
    
    c_click = browser.find_element_by_xpath("")#引号内添加要刷的相应那门课程的xpath
    c_click.click()


    time.sleep(1)
    browser.switch_to.window(browser.window_handles[-1])


# 判断是否有通知
def if_tongzhi():
    time.sleep(1)
    judge = 1
    while judge:
        try:
            cloes_widow = browser.find_element_by_xpath("/html/body/div[9]/div/a")
            cloes_widow.click()
            print(111)
        except:
            print("没有通知弹窗")
            judge = 0
            pass


# 进入视频并且播放
def into_vedio_window():
    time.sleep(1)
    browser.find_element_by_xpath("/html/body/div[5]/div[1]/div[2]/div[3]/div[1]/div[4]/div/h3[2]/span[2]/a").click()#引号内添加从“哪节课开始”的那节课的XPATH
    time.sleep(2)


# 播放视频
def play_vedio():
    time.sleep(1)
    browser.switch_to.frame("iframe")
    # 这里有一个嵌套iframe
    browser.switch_to.frame(0)
    begin_vedio = browser.find_element_by_xpath("//*[@id='video']/button").click()
    time.sleep(3)
    print("课程已经开始播放")


#答题部分不太会就跳过了
def if_question():
    pass


# 判断视频是否完成
def if_vedio_finished():
    time.sleep(1)
    try:
        vedio_stat_time = browser.find_element_by_xpath("//*[@id='video']/div[4]/div[2]/span[2]").get_attribute(
            "textContent")
        vedio_end_time = browser.find_element_by_xpath("//*[@id='video']/div[4]/div[4]/span[2]").get_attribute(
            'textContent')
        print("开始时间和结束时间是:", vedio_stat_time, vedio_end_time)
        time.sleep(10)  # 每10秒检测一次视频是否完成

        return vedio_stat_time, vedio_end_time
    except:
        pass


# 判断是否有第二节课，如果有就播放
def if_have_2nd_class(vedio_stat_time, vedio_end_time):
    if vedio_stat_time == vedio_end_time:
        try:
            # 开始播放第二个视频
            browser.switch_to.default_content()
            browser.switch_to.frame("iframe")
            browser.switch_to.frame(1)
            browser.find_element_by_xpath("//*[@id='video']/button").click()
            time.sleep(3)

        except:
            pass
            print("没有第二节课了")


def start_next(vedio_stat_time, vedio_end_time):
    if vedio_stat_time == vedio_end_time:
        try:
            browser.switch_to.default_content()
            print("开始点下一页")
            browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div[1]/div[8]").click()
            time.sleep(0.5)
            browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div[1]/div[4]").click()
            time.sleep(0.5)
            browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div[1]/div[6]").click()
            time.sleep(0.5)
            browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div[1]/div[8]").click()
            time.sleep(0.5)
        except:
            print("开始点没有小节的下一页")
            browser.switch_to.default_content()
            browser.find_element_by_xpath("//*[@id='mainid']/div[1]/div[2]").click()
            time.sleep(1)
            pass


if __name__ == '__main__':
    input_usename_and_password()
    level_1st()
    if_tongzhi()
    into_vedio_window()
    while True:
        play_vedio()
        time_tuple = if_vedio_finished()
        while time_tuple[0] != time_tuple[1]:
            time_tuple = if_vedio_finished()
            try:
                if_have_2nd_class(time_tuple[0], time_tuple[1])
                if time_tuple[0] == time_tuple[1]:
                    print("开始测试第二节课时间")
                    time_tuple_2 = if_vedio_finished()
                    while time_tuple_2[0] != time_tuple_2[1]:
                        time_tuple_2 = if_vedio_finished()
                        start_next(time_tuple_2[0], time_tuple_2[1])
            except:
                start_next(time_tuple[0], time_tuple[1])
