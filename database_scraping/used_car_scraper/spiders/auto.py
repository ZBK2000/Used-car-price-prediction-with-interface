import scrapy
from scrapy_splash import  SplashRequest

class HasznaltAutoSpider(scrapy.Spider):
    """ This spider goes thru on the 'hasznaltauto.hu' website open all individual url of the cars and takes the wanted details about the ca """


    name = 'auto'
    allowed_domains = ['hasznaltauto.hu']
    start_urls = ['https://www.hasznaltauto.hu/talalatilista/PCOG2VG3R3RDADH5S56ADZJSGMNR454FCZUYKRS2NFPCWQ2NBG4RQJLJGWAPR53V3JJFVFVHLITXM7D4PRJJBMYPPEGTFG2KUEQWESK6YEDGXMLEFSJSEXGQUI4UGFNJQHTFFAAZE5XDV7FAPSARCQYNAWCIWWDO4WSLXJDG3CAM7LLSLX5BBBHPBZOERAMVZ77467R65AVVEV7O4XAMJ7AI3ZLA2RZJWLTPWLSFBEPNYTUBKHQULQRUZUDYNXELGPXLSRMP42AJCXQ467Z5ECUOCGHNAMM2JCYWPEVMYC5KBR5QDU3FNIAH57ZTAYMPUEZDDJA6ZQXJWNGNH2PML7IZ7T7KCDKL6CNSZ7SFL6VR3BURG2PYPMZH66SQV3GYJS47DLQKSHWB6FPCU4TUWUMRLML634K3KP23LXTU2O3AI7SIUHBMVNZVZKKSWZJC7K3IFSKZ6ANHFVK5YHEZMCRUUZDTQJNKKMKY42GSOWWNDXK6LCZ3IEGHXL2OAQAXVVVBKU7ZUZN5ZHQ5DGR3NA6SCF5K6ZJWCV5RRXAZZL7DMMAGJYKMKEXEIJPFK26UM22UUZTNHRG7DNENM4UZ5NPRHTC7GNS6RDSY3AYZNODK4RC77HQSIY5Y64WNPMLDJDTWYPILB7VJLQMAEOKKTM3CA3WYK5FCZJM5ORWM6QNC2RAY52EJGKMERNTM72RB72LFMR336U6VUKFDNBIMPNH6SDB5NQFIFD2TAFP32OUSOOFCHWS55I63TJ3ZJXDX2HSM55PQRRC4A4D2EJNJHIYDPEVIP6D37NF6B5Z2ITM55WRIHMNDKPLM52DO5DBB36JS7QOYAHHVWKZS3P4BP3JKRNXEB5XWB7AHJD5G']
    #start_urls = ['https://www.hasznaltauto.hu/talalatilista/PCOG2VG3R3RDADH5S56ADV5ZQTDVTIKBLKQZCVU227FFAU2CSMMCK2JVQD4PO4O2KINJNJ22Y53HY4T4KKING53Z6FZDZENCQSAAKOIFNOWMLAVRWEKP5DAG6UE2UQANGSJQE5C2XBTPYTMKBXKSUYAIFUIHW2YMVDAWKRWZE4QPY5HALQFKYXHWP72WHIXPMAJHX4DHBM5GIB3QUZVKQSJRN27K6UQU4DAG4FLI4WPRITHCWVAJG7MS4OMRW5FI64MOQSJ2JZLC4Z2GX2DJYOMIYVDI5EQMFXQRBYAADXLZCFB3U3H3LK445YZHIWFKJUH543WKK5Y6QKY5PSOM5PGHUODMNWZDRUH665TX2VMJYTZS7AHV3LNW5AJ5LPXWE5D7MW7F3CYZT4HANXSQHGN7ZKDS6R4GQIRLXSW36RF5H5N5LJ3TVNAE32SVA7XJ3IPGLC5F2IAV33YFAOXIITDVI5YLDII4WXXBCLQJ5JMPSA7KPAOGW5HTDPLCYOUEKSLR4HHIKKVGQN65CWYTIO5WNAEKKGNUE3UK3F6ZKRWGVMBHFD5NGQDLHAJHWF7ELRPFJO6SM3UUVDW3PAJOGSI3J5RTY3PDLGGGO3J4C6FSWB2T2YGG3ANOOLBZXJDQ55TO4Y6HKCM3CKIN3SUVOGR5EYUFGZ6FGSNDHFMRFJLV2GRR4PZTIEDAXARS4JXPZ4S3XOI44IXXC5NUKM74SQQZIWGWLCHL64MWYNBEJVYYNLWYT5LD3QABZUY44TSONNPFQ5G7XESHXKUHHELAD7PRQFUE3FXW4SUBRYVP5XHYEX7SCBSXXF22THSKV4OJ6M2LIJ7U3GHFYAO2BR4F4W4R3HDH62C3DG2AHMWXL5SKNFJ7/page6088']
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint="render.html")

    def parse(self, response):

        linkek = response.xpath('//*[@class="col-xs-28 col-sm-19 cim-kontener"]/h3/a/@href').extract()
        linkek_egyszer =[]
        for i in linkek:
            if i not in linkek_egyszer:
                linkek_egyszer.append(i)

        for szamlalo in range(len(linkek_egyszer)):
            try:
                yield SplashRequest(url=linkek_egyszer[szamlalo], callback=self.parse_links, endpoint="render.html")
            except:
                pass
        try:
            yield SplashRequest(url=response.xpath('//*[@class="next"]/a/@href').extract_first(), callback=self.parse, endpoint="render.html")

        except:
            pass

    def parse_links(self, response):
        # This is a dictionary,which contains the names of the variables, which I wanted to scrape ( precisily as on the website)
        fontos_dolgok_dict={"Évjárat:":"", "Állapot:":"", "Kivitel:":"","Akciós ár:":"", "Vételár:":"", "Vételár EUR:":"", "Üzemanyag:":"", "Hengerűrtartalom:":"","Teljesítmény:":"","Sebességváltó fajtája:":""
            ,"Okmányok jellege:":"","Teljes tömeg:":"","Szín:":"","Hajtás:":"", "Ajtók száma:":"", "Szállítható szem. száma:":"","Kilométeróra állása:":"","Csomagtartó:":"","Klíma fajtája:":"","Műszaki vizsga érvényes:":"" }

        #In this block of code the program searches the variable names and takes the value, which is corresponded to it
        for i in fontos_dolgok_dict:
            for n in response.xpath('//tr'):
                if i ==n.xpath('.//*[@class="bal pontos"]/text()').extract_first():
                    fontos_dolgok_dict[i]= n.xpath('.//strong/text()').extract_first()
        #In the next block of code i had to do some adjusmtents, to get the Brand and the model of the certain car
        nev = response.xpath('//h1/text()').extract_first()
        nev_vegeleges = nev.split()[0]
        tipus = nev.split()[1]
        fontos_dolgok_dict["márka"] = nev_vegeleges
        fontos_dolgok_dict["típus"] = tipus

        yield fontos_dolgok_dict



