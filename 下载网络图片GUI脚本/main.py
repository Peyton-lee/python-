#coding:utf-8

import requests
from bs4 import BeautifulSoup
import os
import re
import uuid
import Tkinter as tk

__author__ = 'peyton'

class GUI():

    def __init__(self):

        # 创建主窗口,用于容纳其它组件
        self.root = tk.Tk()

        # 给主窗口设置标题内容
        self.root.title('根据网址下载图片')

        # 输入一个文本提示
        label = tk.Label(self.root, text='输入网址：')
        label.pack()

        # 创建一个输入框,并设置尺寸
        self.url_input = tk.Entry(self.root, width=70)
        self.url_input.pack()

        # 输入一个文本提示
        labelTwo = tk.Label(self.root, text='输入图片存放目录，例如: ./imgs')
        labelTwo.pack()

        # 创建一个输入框,并设置尺寸
        self.dir_input = tk.Entry(self.root, width=70)
        self.dir_input.insert(0, './imgs')
        self.dir_input.pack()

        # 输入一个下载文本提示
        label = tk.Label(self.root, text='下载结果：')
        label.pack()

        # 创建一个回显列表
        self.display_info = tk.Listbox(self.root, width=90)
        self.display_info.pack()

        # 创建一个下载的按钮
        self.load_button = tk.Button(self.root, command=self.loadImg, text='下载图片', fg='red')
        self.load_button.pack()

    # 下载按钮点击
    def loadImg(self):
        self.display_info.delete(0, tk.END)
        self.display_info.insert(tk.END, '下载中请稍候...')

        # 获取输入图片保存目录
        self._dir = self.dir_input.get()

        if os.path.isdir(self._dir) is False:

            # 判断目录是否存在 不存在就创建
            if os.path.exists(self._dir) is False:
                self.display_info.insert(tk.END, 'create dir name:%s.' % self._dir)
                try:
                    os.mkdir(self._dir)
                except:
                    self.display_info.insert(tk.END, '存放目录有误')
                    return

        # 获取输入地址路径
        self.targetUrl = self.url_input.get()
        self.requestPath([self.targetUrl])
        self.display_info.insert(tk.END, '下载完毕')


    def requestPath(self, url_list):

        # 遍历目标路径查找所有图片路径
        for url in url_list:
            try:
                html = requests.get(url).text
                soup = BeautifulSoup(html, 'html.parser')

                for img in soup.find_all('img'):
                    image = img.get('src')
                    try:
                        self.downLoadImg(image)
                    except IOError:
                        continue
            except IOError:
                self.display_info.insert(tk.END, '网址有误')
                continue


    def downLoadImg(self, url):

        # 获取图片名称
        oldName = url.split('/')[-1]
        suffix = url.split('.')[-1]

        if suffix not in ['jpg', '.jpeg', 'png', 'gif']:
            name = str(uuid.uuid1()) + '__' +oldName + '.jpg'
        else:
            name = str(uuid.uuid1()) + '__' +oldName

        # 组合保存路径
        savePath = os.path.join(self._dir, name)

        # 判断文件名是否存在
        if (os.path.exists(savePath)):
            self.display_info.insert(tk.END, 'file: %s is exist.' % savePath)
            return

        # 判断路径是否含有http字段 没有就加上
        getUrl = re.compile(r'http').match(url) and url or 'http:' + url

        # 下载图片资源
        try:
            ir = requests.get(getUrl, timeout=30)
            if ir.status_code == 200:
                open(savePath, 'wb').write(ir.content)
                self.display_info.insert(tk.END, 'download "%s" successful' % name)
        except:
            pass


if __name__=='__main__':

    # 初始化对象
    FL = GUI()

    # 主程序执行
    tk.mainloop()

