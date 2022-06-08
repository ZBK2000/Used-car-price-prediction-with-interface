import scrapy
from scrapy_splash import  SplashRequest


class HasznaltAutoSpider(scrapy.Spider):

    name = 'auto'
    allowed_domains = ['hasznaltauto.hu']
    start_urls = ['https://www.hasznaltauto.hu/talalatilista/PCOG2VG3R3RDADH5S56ADZJSGMNR454FCZUYKRS2NFPCWQ2NBG4RQJLJGWAPR53V3JJFVFVHLITXM7D4PRJJBMYPPEGTFG2KUEQWESK6YEDGXMLEFSJSEXGQUI4UGFNJQHTFFAAZE5XDV7FAPSARCQYNAWCIWWDO4WSLXJDG3CAM7LLSLX5BBBHPBZOERAMVZ77467R65AVVEV7O4XAMJ7AI3ZLA2RZJWLTPWLSFBEPNYTUBKHQULQRUZUDYNXELGPXLSRMP42AJCXQ467Z5ECUOCGHNAMM2JCYWPEVMYC5KBR5QDU3FNIAH57ZTAYMPUEZDDJA6ZQXJWNGNH2PML7IZ7T7KCDKL6CNSZ7SFL6VR3BURG2PYPMZH66SQV3GYJS47DLQKSHWB6FPCU4TUWUMRLML634K3KP23LXTU2O3AI7SIUHBMVNZVZKKSWZJC7K3IFSKZ6ANHFVK5YHEZMCRUUZDTQJNKKMKY42GSOWWNDXK6LCZ3IEGHXL2OAQAXVVVBKU7ZUZN5ZHQ5DGR3NA6SCF5K6ZJWCV5RRXAZZL7DMMAGJYKMKEXEIJPFK26UM22UUZTNHRG7DNENM4UZ5NPRHTC7GNS6RDSY3AYZNODK4RC77HQSIY5Y64WNPMLDJDTWYPILB7VJLQMAEOKKTM3CA3WYK5FCZJM5ORWM6QNC2RAY52EJGKMERNTM72RB72LFMR336U6VUKFDNBIMPNH6SDB5NQFIFD2TAFP32OUSOOFCHWS55I63TJ3ZJXDX2HSM55PQRRC4A4D2EJNJHIYDPEVIP6D37NF6B5Z2ITM55WRIHMNDKPLM52DO5DBB36JS7QOYAHHVWKZS3P4BP3JKRNXEB5XWB7AHJD5G']

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
                yield scrapy.Request(linkek_egyszer[szamlalo], callback=self.parse_links)
            except:
                pass

        try:
            yield scrapy.Request(response.xpath('//*[@class="next"]/a/@href').extract_first())
        except:
            pass

    def parse_links(self, response):
        fontos_dolgok_dict = {}
        fontos_dolgok=["Évjárat:", "Állapot:", "Kivitel:", "Vételár:", "Vételár EUR:", "Üzemanyag:", "Hengerűrtartalom:","Teljesítmény:","Sebességváltó fajtája:"
            ,"Okmányok jellege:","Teljes tömeg:","Szín:","Hajtás:", "Ajtók száma:", "Szállítható szem. száma:","Kilométeróra állása:","Csomagtartó:","Klíma fajtája:","Műszaki vizsga érvényes:" ]
        for i in fontos_dolgok:
            for n in response.xpath('//tr'):
                if i ==n.xpath('.//*[@class="bal pontos"]/text()').extract_first():
                    fontos_dolgok_dict[i]= n.xpath('.//strong/text()').extract_first()
        nev = response.xpath('//h1/text()').extract_first()
        nev_vegeleges = nev.split()[0]
        tipus = nev.split()[1]
        fontos_dolgok_dict["márka"] = nev_vegeleges
        fontos_dolgok_dict["típus"] = tipus

        yield fontos_dolgok_dict



