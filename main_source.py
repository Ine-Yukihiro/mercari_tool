import tkinter
from tkinter import messagebox
from tkinter import ttk
from selenium import webdriver
import os
import time
import webbrowser
import requests

class GUI() :
    def __init__(self) :
        self.root = tkinter.Tk()
        self.root.geometry("400x300")
        self.root.title("mercari_tool v1.0")

        def MakeMenubar() :
            self.menubar = tkinter.Menu(self.root)
            self.root.config(menu=self.menubar)

            self.menu_1 = tkinter.Menu(self.root)
            self.menubar.add_cascade(label="--", menu = self.menu_1)
        MakeMenubar()

    def MakeFrame_main(self) :
        self.frame = tkinter.Frame(self.root)
        self.frame.pack(fill = tkinter.BOTH, pady=4)

        def MakeWidgets() :
            self.label_listingitemstitle = ttk.Label(self.frame, text = "出品中の商品", relief = "groove")
            def MakeTreeview_listingitems() :
                self.treeview_listingitems = ttk.Treeview(
                    self.frame,
                    columns = (1, 2, 3),
                    show = "headings")

                self.treeview_listingitems.column (1, width = 280)
                self.treeview_listingitems.heading(1, text = "商品名")
                self.treeview_listingitems.column (2, width = 50)
                self.treeview_listingitems.heading(2, text = "いいね数")
                self.treeview_listingitems.column (3, width = 50)
                self.treeview_listingitems.heading(3, text = "ｺﾒﾝﾄ数")
            MakeTreeview_listingitems()
            self.button_reloadlistingitems = ttk.Button(self.frame, text = "更新")
            self.button_relistselecteditem = ttk.Button(self.frame, text = "再出品", command = pressed_button_relistselecteditem)
        def PackWidgets() :
            self.label_listingitemstitle.pack()
            self.treeview_listingitems.pack()
            self.button_reloadlistingitems.pack(fill = "x", side = "left")
            self.button_relistselecteditem.pack(fill = "x", side = "left")
        
        MakeWidgets()
        PackWidgets()

    def ItemFocusedCheck(self) :
        self.focused_item = gui.treeview_listingitems.selection()
        if len(self.focused_item) == True :
            return gui.treeview_listingitems.item(self.focused_item[0])['values'][3]
        else :
            messagebox.showinfo("error", "商品を選択してください")
            return ""

class WebDriver() :
    def __init__(self, on_headless) :
        self.profile_dir="profiles"
        os.makedirs(self.profile_dir, exist_ok=True)
        self.options = webdriver.ChromeOptions()
        self.profile_path = 'C:\\Users\\' + os.getlogin() + '\\AppData\\Local\\Google\\Chrome\\User Data'
        self.options.add_argument('--user-data-dir=' + self.profile_path)
        self.chromedriver_path = "chromedriver.exe"
        self.chrome = webdriver.Chrome(executable_path=self.chromedriver_path, options=self.options)
        
    def Login_mercari(self) :
        self.mercari_listingitems_URL = "https://www.mercari.com/jp/mypage/listings/listing/"
        self.chrome.get(self.mercari_listingitems_URL)
        time.sleep(1)
        return not ("ログイン" in self.chrome.title)

    def GetListingItemsMax(self) :
        self.elements_listingitemsinfo_max = self.chrome.find_elements_by_class_name("mypage-item-link")
        self.listingitemsmax = len(self.elements_listingitemsinfo_max)

    def GetListingItemsInfo(self, get_index) :
        def ScrapeListingItemInfo() :
            self.listingitemsinfo_name = self.chrome.find_elements_by_class_name("mypage-item-text")[get_index].text
            self.listingitemsinfo_like = self.chrome.find_elements_by_css_selector("span.listing-item-count:nth-child(1) > span:nth-child(2)")[get_index].text
            self.listingitemsinfo_comm = self.chrome.find_elements_by_css_selector("span.listing-item-count:nth-child(2) > span:nth-child(2)")[get_index].text
            self.listingitemsinfo_url  = self.chrome.find_elements_by_class_name("mypage-item-link")[get_index].get_attribute("href")
        ScrapeListingItemInfo()

        self.return_value = [self.listingitemsinfo_name, self.listingitemsinfo_like, self.listingitemsinfo_comm, self.listingitemsinfo_url]
        print(self.return_value)

        return self.return_value

    def GetSelectedItemInfo(self, selecteditem_URL) :
        self.chrome.get(selecteditem_URL)
        time.sleep(2)
        def ScrapeRelistItemInfo() :
            for i in range(len(self.chrome.find_elements_by_class_name("owl-dot"))) :
               self.item_image = self.chrome.find_element_by_css_selector("div.owl-dot:nth-child(" + str(i + 1) + ") > div:nth-child(2) > img:nth-child(1)").get_attribute("src")
               print(self.item_image)

            self.item_name = self.chrome.find_element_by_css_selector(".item-name").text
            self.item_category1 = self.chrome.find_element_by_css_selector(".item-detail-table > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > a:nth-child(1) > div:nth-child(1)").text
            self.item_category2 = self.chrome.find_element_by_css_selector(".item-detail-table-sub-category").text
            self.item_category3 = self.chrome.find_element_by_css_selector(".item-detail-table-sub-sub-category").text
            self.item_brand = self.chrome.find_element_by_css_selector(".item-detail-table > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2)").text
            self.item_condition = self.chrome.find_element_by_css_selector(".item-detail-table > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(2)").text
            self.item_burden = self.chrome.find_element_by_css_selector(".item-detail-table > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(2)").text
            self.item_method = self.chrome.find_element_by_css_selector(".item-detail-table > tbody:nth-child(1) > tr:nth-child(6) > td:nth-child(2)").text
            self.item_prefecture = self.chrome.find_element_by_css_selector(".item-detail-table > tbody:nth-child(1) > tr:nth-child(7) > td:nth-child(2)").text
            self.item_days = self.chrome.find_element_by_css_selector(".item-detail-table > tbody:nth-child(1) > tr:nth-child(8) > td:nth-child(2)").text
            self.item_price = self.chrome.find_element_by_css_selector(".item-price").text.replace('¥', '')
            self.item_description = self.chrome.find_element_by_css_selector(".item-description-inner").text
            print(self.item_name, self.item_category1, self.item_category2, self.item_category3, self.item_brand, self.item_condition, self.item_burden, self.item_method, self.item_prefecture, self.item_days, self.item_price)
            print(self.item_description)
        ScrapeRelistItemInfo()

        # self.chrome.get(selecteditem_URL.replace('mypage', 'sell').replace('items', 'edit'))

        self.chrome.get("https://www.mercari.com/jp/sell")
        def InputRelistItemData() :
            self.chrome.find_element_by_xpath( "//input[@type='file']" ).send_keys("C:\\Users\\motoi\\Downloads\\title_logo.png")
        InputRelistItemData()

if __name__ == "__main__" :
    debug = True
    webdriver = WebDriver(True)
    gui = GUI()
    if webdriver.Login_mercari() == True : # Succeeded login mercari
        def pressed_button_relistselecteditem() :
            ret = gui.ItemFocusedCheck()
            if ret != "" :
                if messagebox.askyesno("askyesno", "選択した商品を再出品してよろしいですか") == True:
                    def RelistItem(item_url) :
                        webdriver.GetSelectedItemInfo(item_url)
                    RelistItem(ret)                
        gui.MakeFrame_main()
        def AddItemsToTreeView() :
            webdriver.GetListingItemsMax()
            for cnt in range(webdriver.listingitemsmax) :
                gui.treeview_listingitems.insert("", "end", values = (webdriver.GetListingItemsInfo(cnt)))
        AddItemsToTreeView()
    else : # Failed login mercari
        def ManualLoginMercari() :
            dialog_text = "メルカリのログインがされていません。\nChromeを起動し、手動操作によりメルカリのログインを完了させた後、アプリケーションを再起動してください。"
            messagebox.showinfo("showinfo", dialog_text)

            manual_chrome = webbrowser.get('chrome')
            manual_chrome.open("https://www.mercari.com/jp/login/?login_callback=%2Fjp%2F")

            exit()
        ManualLoginMercari() # Have the user log in manually

    gui.root.mainloop()