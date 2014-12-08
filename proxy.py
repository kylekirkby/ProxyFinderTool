from urllib.request import urlopen, URLopener
from bs4 import BeautifulSoup

from PyQt4.QtCore import *


class ProxyList(QThread):

    complete = pyqtSignal(list)

    """ This class gathers the proxy information"""

    def __init__(self):

        QThread.__init__(self)

        self.url = "http://proxy-list.org/english/index.php?p="

        self.proxies = []

    
    def getList(self,url):
        soup = urlopen(url).read()
        
        page = BeautifulSoup(soup)

        proxyTable = page.find("div",{"class":"table"})

        uls = proxyTable.findAll("ul")

        for ul in uls:
            
            newProxy = []
            
            proxy = ul.find("li",{"class":"proxy"})
            https = ul.find("li",{"class":"https"})
            speed = ul.find("li",{"class":"speed"})
            proxyType = ul.find("li",{"class":"type"})
            country = ul.find("span",{"class":"name"})
            countryCity = ul.find("span",{"class":"city"})
            
            strongSearch = https.find("strong")
            if strongSearch == None:
                connectionType = "HTTP"
            else:
                connectionType = "HTTPS"


            strongSearch2 = proxyType.find("strong")
            if strongSearch2 == None:
                typeOfProxy  = proxyType.contents[0]

            else:
                typeOfProxy = strongSearch2.contents[0]
                
            countryCity2 = countryCity.find("span")

            
            city = countryCity2.contents[0]
            city = city.replace(u'\xa0', u' ')
            
            newProxy.append(proxy.contents[0])
            newProxy.append(connectionType)
            newProxy.append(speed.contents[0])
            newProxy.append(typeOfProxy)
            newProxy.append(country.contents[0])
            newProxy.append(city)

            self.proxies.append(newProxy)
            
    def kill(self):
        print("killed")

    def getProxies(self):

        for i in range(1,11):
            newUrl = self.url + str(i)
            self.getList(newUrl)
            
        return self.proxies


    def run(self):
        results = self.getProxies()
        self.complete.emit(results)
        
        


        

if __name__ == "__main__":
    
    #example usage
    pl = ProxyList()
    pl.getProxies()
