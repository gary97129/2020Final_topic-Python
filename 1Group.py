import tkinter as tk  
import tkinter.ttk as tt
import requests as rq
from bs4  import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
from PIL import Image
import cv2
import pyocr
import pyocr.builders
import numpy as np

start=0
load = "Loading . . ."
loadtime = 2

def window1():
    def select():
        load = "Loading . . ."
        lab['text'] = load[0:1]
        loadtime = 2
        start = time.time()
        def form(url,key,value):
            table = url.find('table', {key: value})
            columns=[]
            for th in table.find('tr').find_all('th'):
                tim()
                columns.append(th.text.replace('\n', ''))
            return table.find_all('tr')[1:]
        
        def tim():
            global start,loadtime
            if int(time.time()) - start  > 0.5:
                lab['text'] = load[0:loadtime]
                if loadtime == 7 or loadtime == 8 or loadtime == 11:loadtime+=2
                elif loadtime != 13:loadtime+=1
                else:loadtime=1
                window1.update()
                start = time.time()
    
        def add(rows):
            t=0
            while t != len(rows):
                tim()
                if rows[t][0]== '2357':
                    tt=0
                tt=0
                url = rq.get("http://jsjustweb.jihsun.com.tw/z/zc/zca/zca_" + rows[t][0] +".djhtm")
                url = bs(url.text,"html.parser")
                trs = form(url,'class','t01')
                for tr in trs:
                    tim()
                    s=[]
                    for td in tr.find_all('td'):
                        tim()
                        s.append(td.text.replace('\n', '').replace('\xa0', '').replace('　', ' ').replace(',', ''))
                    if len(s) == 8:   
                        if s[6] == "收盤價" :
                            if s[7] == 'N/A':del rows[t];break
                            rows[t].append(s[7])
                    if s[0] == "本益比" :
                        if s[1] == 'N/A':del rows[t];break
                        rows[t].append(s[1])
                    if s[0] == "同業平均本益比":
                        if s[1] == 'N/A': del rows[t];break
                        if eval(rows[t][-1]) >= eval(s[1]):del rows[t];break
                    if len(s) == 6:
                        if s[4] == "股東權益報酬率" :
                            if s[5] == 'N/A':del rows[t];break
                            if eval(s[5][:-1])<=5:del rows[t];break
                            rows[t].append(s[5])       
                            url = rq.get("http://jsjustweb.jihsun.com.tw/z/zc/zcq/zcq_" + rows[t][0] +".djhtm")
                            url = bs(url.text,"html.parser")
                            trs = form(url,'class','t01')
                            for tr in trs:
                                tim()
                                s=[]
                                for td in tr.find_all('td'):
                                    tim()
                                    s.append(td.text.replace('\n', '').replace('\xa0', '').replace('　', ' ').replace(',', ''))
                                if s[0] == "營業外收入及支出" :
                                    if s[1] == 'N/A':del rows[t];break
                                    rows[t].append(s[1])
                                if s[0] == "每股盈餘" :
                                    if s[1] == 'N/A':del rows[t];break
                                    if eval(rows[t][-1])*4 >= eval(s[1]): del rows[t];break
                                    rows[t][-1] = s[1]
                                    t+=1
                                    break
                            break
        
        
        def speed(rows):
            t=0
            while t != len(rows):
                tim()
                url = rq.get("https://www.cnyes.com/twstock/ps_historyprice.aspx?code=" + rows[t][0])
                url = bs(url.text,"html.parser")
                try:
                    trs = form(url,'enableviewstate','false')
                    po = [0]
                    for tr in trs:
                        tim()
                        s=[]
                        for td in tr.find_all('td'):
                            tim()
                            s.append(td.text.replace('\n', '').replace('\xa0', '').replace('　', ' ').replace(',', '') )
                        po.append(eval("%.2f"%((eval(s[2])+eval(s[3]))/2)))
                    if (len(po)-1) % 2 == 0:
                        end = len(po)-1
                    else:
                        end = len(po)-2
                    close20 = (po[1] + po[end])/2>po[int(end/2)]
                    if not(close20):
                        del rows[t]
                    else:
                        t+=1
                except:
                    del rows[t]
                      
                        
        def mine():
            url = rq.get("https://isin.twse.com.tw/isin/C_public.jsp?strMode=2")
            url = bs(url.text,"html.parser")
            table = url.find('table', {'class': 'h4'})
            columns=[]
            for th in table.find('tr').find_all('th'):
                tim()
                columns.append(th.text.replace('\n', '') )
            trs = table.find_all('tr')[1:]
            rows = []
            for tr in trs:
                tim()
                s=[]
                for td in tr.find_all('td'):
                    tim()
                    s.append(td.text.replace('\n', '').replace('\xa0', '').replace('　', ' ') )
                if len(s) == 7 : 
                    if s[4] == "" : break
                    ss = s[0] + " " + s[4] ; rows.append(ss.split(" "))
                    
            add(rows)
            speed(rows)
            
            sid=[]
            for i in rows:
                tim()
                sid.append([i[0],i[1],i[3],i[2][:-1]])
            items = tree.get_children()
            for i in items:
                tim()
                tree.delete(i)
            for i in sid: 
                tim()
                tree.insert("",'end',values=i)
              
            vbar.config(command = tree.yview)
            lab['text'] = "      完成      "
                
        mine()
    window1 = tk.Tk()       
    window1.title('自動選股')
    window1.state("zoomed")
    window1.resizable(1,1) 
    window1.config(bg="#F5DEB3")
    window1.attributes("-alpha",1)
    #-------------------------------------------------------------------------------
    btn = tk.Button(window1,text='選  股',activebackground='#FFFFF0',font='PMingLiU 30', command= lambda: select())
    btn.place(relx=0.45,rely=0.01)
    
    lab = tk.Label(window1,text="",font='PMingLiU 30',bg = "#F5DEB3")
    lab.place(relx=0.43,rely=0.13)
    
    vbar = tk.Scrollbar(window1)
    vbar.place(relx=0.692,rely=0.22,height = 606)
    
    tree = tt.Treeview(window1)
    tree.place(relx=0.3,rely=0.22)
    
    tree['columns'] = (1,2,3,4)
    tree.column(1, width=100, anchor='center')
    tree.column(2, width=200, anchor='center')
    tree.column(3, width=100, anchor='center')
    tree.column(4, width=200, anchor='center')
    tree.heading(1, text = "股票代號")
    tree.heading(2, text = "股票名稱")
    tree.heading(3, text = "價格")
    tree.heading(4, text = "行業")
    tree['show'] = 'headings'
    tree["height"] = 29
    tree['yscrollcommand'] = vbar.set
    
    window1.mainloop()
    
    
    
def window2():
           
    window2 = tk.Tk()            #宣告window為視窗物件
    window2.title('天氣預報')   #設定視窗標題
    
    #視窗大小
    window2.geometry("700x600")             #寬x高
    #window1.minsize(width=400,height=320)   #最小範圍
    #window1.maxsize(width=1024,height=768)  #最大範圍
    window2.resizable(0,0) #1=True,0=False  是否調整大小 resizable(width,height)
    
    #顏色
    window2.config(bg="#F5DEB3")       #config(bg='背景顏色') 可以填入顏色或是色碼
    
    #透明度
    window2.attributes("-alpha",1)   #1~0 1是100%完全不透明 0是0%透明，可以輸入小數點
    
    #視窗至頂
    #window2.attributes("-topmost",1)#1=True,0=False
    #-------------------------------------------------------------------------------
    def weather(c):
        #定義b為城市網址代碼
        b=['0','10017','63','65','68','10018','10004','10005','66','10007','10008','10009','10020','10010','67','64','10013','10002','10015','10014','10016','09020','09007']
        #自動化搜尋中央氣象局網站的城市天氣資料
        google_path = Options()
        google_path.add_argument("--disable-notifications")        
        driver = webdriver.Chrome('./chromedriver', chrome_options=google_path)
        #進入網站
        driver.get("https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=%s"%b[c])
        driver.minimize_window()
        while 1:
            #抓取網站資訊，今日白天溫度
            z1=driver.find_element_by_xpath("/html/body/div[2]/main/div/div[2]/div[3]/div/div[1]/div[1]/table/tbody/tr[1]/td[1]/p/span[1]")
            #抓取網站資訊，今日晚上溫度
            z2=driver.find_element_by_xpath("/html/body/div[2]/main/div/div[2]/div[3]/div/div[1]/div[1]/table/tbody/tr[2]/td[1]/p/span[1]")
            #抓取網站資訊，今日體感溫度
            z4=driver.find_element_by_xpath("/html/body/div[2]/main/div/div[2]/div[3]/div/div[1]/div[1]/table/tbody/tr[3]/td[1]/span[1]")
            #抓取網站資訊，明日白天溫度
            z5=driver.find_element_by_xpath("/html/body/div[2]/main/div/div[2]/div[3]/div/div[1]/div[1]/table/tbody/tr[1]/td[2]/p/span[1]")
            #抓取網站資訊，明日晚上溫度
            z6=driver.find_element_by_xpath("/html/body/div[2]/main/div/div[2]/div[3]/div/div[1]/div[1]/table/tbody/tr[2]/td[2]/p/span[1]")
            #抓取網站資訊，明日體感溫度
            z8=driver.find_element_by_xpath("/html/body/div[2]/main/div/div[2]/div[3]/div/div[1]/div[1]/table/tbody/tr[3]/td[2]/span[1]")
            #抓取網站資訊，降雨機率
            ss =driver.page_source.split('<i title="降雨機率" class="icon-umbrella" aria-hidden="true"></i>')[1:3]
            z3="";z7=""
            for i in range(2):
                for j in ss[i]:
                    if j != '<':
                        if i==0:z3 += j
                        elif i == 1:z7+=j
                    else:break
            if z1 != "" and  z2 != "" and  z3 != "" and z4 != "" and z5 != "" and z6 != "" and z7 != "" and z8 != "":break 
        window2_1 = tk.Tk()   
        window2_1.title('天氣預報')
        
        #視窗大小
        window2_1.geometry("450x380")             #寬x高
        #window1.minsize(width=400,height=320)   #最小範圍
        #window1.maxsize(width=1024,height=768)  #最大範圍
        window2_1.resizable(0,0) #1=True,0=False  是否調整大小 resizable(width,height)
        
        #顏色
        window2_1.config(bg="#F5DEB3")       #config(bg='背景顏色') 可以填入顏色或是色碼
        
        #透明度
        window2_1.attributes("-alpha",1)   #1~0 
        
        ss ="今日白天溫度：%s℃\n今日晚上溫度：%s℃\n今日降雨機率：%s\n今日體感溫度：%s℃\n----------------------------------\n明日白天溫度：%s℃\n明日晚上溫度：%s℃\n明日降雨機率：%s\n明日體感溫度：%s℃"%(z1.text,z2.text,z3,z4.text,z5.text,z6.text,z7,z8.text)
        
        lab = tk.Label(window2_1,text=ss,font='PMingLiU 30',bg = "#F5DEB3")
        lab.place(relx=0,rely=0)
        driver.quit()
        window2_1.mainloop()
    
    

    #---------------------------------------------------------------------------
    tw=['1','基隆市','2', '臺北市',  '3', '新北市',  '4', '桃園市',  '5', '新竹市', '6', '新竹縣' , '7' ,'苗栗縣' , '8', '臺中市'  ,'9', '彰化縣', '10' ,'南投縣','11', '雲林縣', '12' ,'嘉義市', '13' ,'嘉義縣', '14' ,'臺南市', '15', '高雄市', '16','屏東縣', '17' ,'宜蘭縣', '18', '花蓮縣', '19', '臺東縣', '20', '澎湖縣','21', '金門縣', '22' ,'連江縣']
    xy=1
    y1=0             
    while 1 :
        if y1 >= 10:break
        x1=0
        while 1:
            if x1 >= 10:break
            bu1 = tk.Button(window2,text=tw[xy],bg = 'white',fg = '#5B5B5B',activeforeground = "black",activebackground='#E0E0E0',font='PMingLiU 20', command=lambda s1=eval(tw[xy-1]) : weather(s1))
            bu1.place(relx=x1/10+0.03,rely=y1/10+0.09)
            x1 +=10/4
            xy+=2
            if xy > len(tw):break
        y1+=10/7
        if xy > len(tw):break
    
    #--------------------------------------------------------------------------------

    
    
    window2.mainloop()             #循環常駐主視窗
    
    
def window3():
    window3 = tk.Tk()
    window3.title('一鍵下載音樂清單')
    window3.state("zoomed")
    window3.resizable(1,1)
    window3.config(bg="#F5DEB3")
    window3.attributes("-alpha",1)
    #-------------------------------------------------------------------------------   
    def downloads(urls):
        items = tree.get_children()
        for i in items:
            tree.delete(i)
        try:
            urls = urls.replace(" ","")
            if urls[:29] == "https://www.youtube.com/watch":
                
                path = os.path.dirname(__file__)
                google_path = Options()
                prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': path}
                google_path.add_experimental_option('prefs', prefs)
                google_path.add_argument("--disable-notifications")
                
                driver = webdriver.Chrome('./chromedriver', chrome_options=google_path)
                driver.get(urls)
                driver.minimize_window()
                driver.implicitly_wait(10)
                
                url = driver.find_elements_by_xpath('//*[@id="wc-endpoint"]')
                url = [i.get_attribute('href')  for i in url]
                lab2['text'] = "下載中 0 / " + str(len(url))  
                window3.update()  
                id1 = [];id2 =[];id_=1
                for i in url:
                    try:
                        driver.get("https://yt1s.com/youtube-to-mp3/zh-tw")
                        driver.implicitly_wait(10)
                        ac = driver.find_element_by_xpath('//*[@id="s_input"]')
                        ac.send_keys(i)
                        downbtn = driver.find_element_by_xpath('//*[@id="search-form"]/button')
                        downbtn.click()
                        driver.implicitly_wait(10)
                        while 1:
                            down = driver.find_element_by_xpath('//*[@id="asuccess"]')
                            if 'yt1s.com' not in down.get_attribute('href') :break
                        driver.get(down.get_attribute('href'))
                        id1.append("第" + str(id_) + "首")
                    except:
                        id2.append("第" + str(id_) + "首")
                        
                    lab2['text'] = "下載中 " + str(id_) +" / "+ str(len(url)) 
                    window3.update()
                    id_+=1
                lab2['text'] = " 即將完成" 
                window3.update()
                s=1
                while s:
                    s=0
                    for i in os.listdir(path):
                        if i[-10:] == "crdownload" : 
                            s=1
                        else:
                            if i[:11] == "yt1s.com - ":
                                ind = " ";ii=i[11:]
                                while ii in os.listdir(path):
                                    ii=ii[:-4] + ind + ii[-4:]
                                os.rename(os.path.join(path, i), os.path.join(path, ii))                               
                driver.quit()
                while 1:
                    if len(id1)>len(id2):id2.append("")
                    elif len(id1)<len(id2):id1.append("")
                    else:break
                for i in range(len(id1)):
                    tree.insert("",'end',values=[id1[i],id2[i]])
                vbar.config(command = tree.yview)
                lab2['text'] = "下載已完成"
                ttext.delete(0, 'end')
            else:lab2['text'] = "輸入有錯誤"
        except:
            lab2['text'] = "輸入有錯誤"
    #-------------------------------------------------------------------------------
    lab1 = tk.Label(window3,text="一鍵下載音樂清單",font='PMingLiU 50',bg = "#F5DEB3",fg = 'red')
    lab1.place(relx=0.315,rely=0.2)
    lab2 = tk.Label(window3,text="請輸入網址",font='PMingLiU 30',bg = "#F5DEB3")
    lab2.place(relx=0.425,rely=0.38)
    
    vbar = tk.Scrollbar(window3)
    vbar.place(relx=0.593,rely=0.7,height = 200)

    tree = tt.Treeview(window3)
    tree.place(relx=0.39,rely=0.7,height = 200)
    
    tree["columns"] = (1,2)
    tree.column(1, width=155)
    tree.column(2, width=155)
    tree.heading(1, text="下載成功")
    tree.heading(2, text="下載失敗")
    tree['show'] = 'headings'
    tree['yscrollcommand'] = vbar.set
    ttext = tk.Entry(window3 ,bd=5,width = 45, font='PMingLiU 30')
    ttext.place(relx=0.22,rely=0.455)
    btn = tk.Button(window3,text='Download',activebackground='#FFFFF0',font='PMingLiU 25', command= lambda: downloads(ttext.get()))
    btn.place(relx=0.44,rely=0.6)
    #------------------------------------------------------------------------------  
    window3.mainloop()  


def window4():
    window4 = tk.Tk()
    window4.title('自 動 登 入')
    window4.geometry("400x400")
    window4.resizable(0,0)    
    window4.attributes("-alpha",1)
    def wab(netcode,account,password):

        urls={"0":"https://ecare.nfu.edu.tw/",#ecare
              "1":"https://e3.nfu.edu.tw/EasyE3P/LMS2/login.aspx",#e3
              "2":"http://flipped.nfu.edu.tw/service/login?next=%2F"}#翻轉
        
        acbox_xpath={"0":'//*[@id="login_acc"]',
                     "1":'//*[@id="txtLoginId"]',
                     "2":'//*[@id="mod_service_0_account"]'}
        
        psdbox_xpath={"0":'//*[@id="login_pwd"]',
                      "1":'//*[@id="txtLoginPwd"]',
                      "2":'//*[@id="mod_service_0_password"]'}
        
        vercodebox_xpath={"0":'//*[@id="login_chksum"]',
                          "1":'//*[@id="txtCheck"]',
                          "2":'//*[@id="mod_service_0_captcha"]'}
        
        vercodeimg_xpath={"0":'//*[@id="authimg"]',
                       "1":'//*[@id="imgCheck"]',
                       "2":'//*[@id="xbox-inline"]/div/div/div[2]/div[1]/div[1]/div[3]/div[2]/img'}
        
        loginbtn_xpath={"0":'//*[@id="bt_login"]',
                        "1":'//*[@id="btnLogin"]',
                        "2":'/html/body/div[2]/div[3]/div[2]/div/div/div[2]/div[1]/div[2]/button'}
        
        lowerred_dict={"0":[0,43,46],
                       "2":[100,125,46]}
        
        upperred_dict={"0":[14,255,255],
                       "2":[124,255,255]}
        
        google_path = Options()
        google_path.add_argument("--disable-notifications")
        
        driver = webdriver.Chrome('./chromedriver', chrome_options=google_path)
        
        def run():
            driver.get(urls[netcode])
            driver.implicitly_wait(10)
            
            accountbox = driver.find_element_by_xpath(acbox_xpath[netcode])
            accountbox.send_keys(account)
            
            passwordbox = driver.find_element_by_xpath(psdbox_xpath[netcode])
            passwordbox.send_keys(password)
            
            driver.save_screenshot("123.png")#截圖
            
            Web_Verification_code_img=driver.find_element_by_xpath(vercodeimg_xpath[netcode])#裁切
            x1=Web_Verification_code_img.location["x"]
            x2=Web_Verification_code_img.location["x"]+Web_Verification_code_img.size["width"]
            y1=Web_Verification_code_img.location["y"]
            y2=Web_Verification_code_img.location["y"]+Web_Verification_code_img.size["height"]
            pict=Image.open("123.png")
            if netcode=="1":
                croppict=pict.crop((x1+1,y1+1,x2-1,y2-1))
            else:
                croppict=pict.crop((x1,y1,x2,y2))
            croppict.save("123.png")
            
            img=cv2.imread("123.png")#放大
            h,w,_ = img.shape
            img_resize = cv2.resize(img,(w*5,h*5))
            
            if netcode == '0': #旋轉
                h,w,_ = img_resize.shape
                M = cv2.getRotationMatrix2D((w/2,h/2),356,1)
                img_resize = cv2.warpAffine(img_resize,M,(w,h))
            
            if netcode=='0' or netcode=="2":#製作mask
                imgHSV = cv2.cvtColor(img_resize,cv2.COLOR_BGR2HSV)
                lower_red = np.array(lowerred_dict[netcode])
                upper_red = np.array(upperred_dict[netcode])
                mask = cv2.inRange(imgHSV,lower_red,upper_red)
        
            
            if netcode=="1":
                cv2.imwrite("123.png",img_resize)
            else:
                cv2.imwrite("123.png",mask)
            
            
            tools=pyocr.get_available_tools()
            if len(tools)==0:
                print("No found OCR any tool!!!!!!!!!")
                
            tool=tools[0]
            
            img = Image.open("123.png")
            txt = tool.image_to_string(img,lang="eng",builder=pyocr.builders.TextBuilder())
            txt=txt.replace(" ", "")
            print("辨識到的驗證碼："+txt)
            
            
            if len(list(filter(str.isalnum, txt))) == 4:
                Verificationcodebox=driver.find_element_by_xpath(vercodebox_xpath[netcode])
                Verificationcodebox.send_keys(txt)
                    
                loginbtn=driver.find_element_by_xpath(loginbtn_xpath[netcode])
                loginbtn.click()
            else:
                run()
        
        
        run()
        
        while 1:
            if netcode=="0":
                if driver.current_url=="https://ecare.nfu.edu.tw/login/auth":
                    try:
                        if driver.find_element_by_xpath('/html/body/div[1]/div[1]/section[2]/div/div/h4').text=="認證碼輸入有誤~~~~":
                            run()
                    except:
                        break
                elif driver.current_url=="https://ecare.nfu.edu.tw/desktop":
                    break
            elif netcode=="1":
                if driver.current_url=="https://e3.nfu.edu.tw/EasyE3P/LMS2/login.aspx":
                    error=driver.find_element_by_xpath('//*[@id="lblCheckMessage"]')
                    if error.is_displayed():
                        run()
                    else:
                        break
            elif netcode=="2":
                if driver.current_url=="http://flipped.nfu.edu.tw/service/login?next=%2F":
                    error=driver.find_element_by_xpath('//*[@id="xbox-inline"]/div/div/div[2]/div[1]/div[1]/div[3]/div[2]/span/div')
                    if error.is_displayed():
                        run()
                    else:
                        break
    def inp(netcode):
        
        window4_1 = tk.Tk()
        window4_1.title('登入')
        window4_1.config(bg="#F5DEB3")
        window4_1.geometry("500x150")
        window4_1.resizable(0,0)    
        window4_1.attributes("-alpha",1) 
        
        lab1 = tk.Label(window4_1,text='帳號 :',bg='#F5DEB3',font='PMingLiU 20')
        lab1.place(relx=0.1,rely=0.1)
        
        account = tk.Entry(window4_1, width=23,font = 'PMingLiU 20')
        account.place(relx=0.3,rely=0.1)
        
        lab2 = tk.Label(window4_1,text='密碼 :',bg='#F5DEB3',font='PMingLiU 20')
        lab2.place(relx=0.1,rely=0.4)
        
        password = tk.Entry(window4_1, show='*',  width=23,font = 'PMingLiU 20')
        password.place(relx=0.3,rely=0.4)
        
        btn = tk.Button(window4_1,text='登 入',fg = '#5B5B5B',activeforeground = "black",activebackground='#E0E0E0',font='PMingLiU 15', command= lambda: wab(netcode,account.get(),password.get()))
        btn.place(relx=0.45,rely=0.7)
    
        window4_1.mainloop() 
        
    ap1 = tk.Button(window4,text='登入ecare',width = 14,height = 7 ,bg = 'white',fg = '#5B5B5B',activeforeground = "black",activebackground='#E0E0E0',font='PMingLiU 20', command= lambda: inp('0'))
    ap1.place(relx=-0,rely=0) 
    
    ap2 = tk.Button(window4,text='登入e3',width = 14,height = 7,bg = 'white',fg = '#5B5B5B',activebackground='#E0E0E0',font='PMingLiU 20', command= lambda: inp('1'))
    ap2.place(relx=0.5,rely=0)
    
    ap3 = tk.Button(window4,text='登入翻轉',height = 7,width = 28,bg = 'white',fg = '#5B5B5B',activebackground='#E0E0E0',font='PMingLiU 20', command= lambda: inp('2'))
    ap3.place(relx=0,rely=0.52)
    

    window4.mainloop()               

window = tk.Tk()            
window.title('選單') 
window.geometry("400x400")
window.resizable(0,0)    
window.attributes("-alpha",1)   
    
ap1 = tk.Button(window,text='自 動 選 股',width = 14,height = 7 ,bg = 'white',fg = '#5B5B5B',activeforeground = "black",activebackground='#E0E0E0',font='PMingLiU 20', command= lambda: window1())
ap1.place(relx=-0,rely=0) 

ap2 = tk.Button(window,text='天 氣 預 報',width = 14,height = 7,bg = 'white',fg = '#5B5B5B',activebackground='#E0E0E0',font='PMingLiU 20', command= lambda: window2())
ap2.place(relx=0.5,rely=0)

ap3 = tk.Button(window,text='一 鍵 下 載\n音 樂 清 單',width = 14,height = 7,bg = 'white',fg = '#5B5B5B',activebackground='#E0E0E0',font='PMingLiU 20', command= lambda: window3())
ap3.place(relx=0,rely=0.5) 

ap4 = tk.Button(window,text='學 校 網 站\n自 動 登 入',width = 14,height = 7,bg = 'white',fg = '#5B5B5B',activebackground='#E0E0E0',font='PMingLiU 20', command= lambda: window4())
ap4.place(relx=0.5,rely=0.5) 

window.mainloop()