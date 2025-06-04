import pandas as pd
import numpy as np

df = pd.read_excel(r"C:\Users\HP\PycharmProjects\PythonProject\gezinomi_tanıtım\miuul_gezinomi.xlsx")
df.head()
pd.set_option('display.max_columns', None)
pd.set_option('display.width',500)

#Soru2:Kaç unique şehirvardır? Frekanslarınedir
df["SaleCityName"].unique()
df["SaleCityName"].value_counts()

# Soru3:Kaç unique Concept vardır?
df["ConceptName"].nunique()

#Soru4: Hangi Concept’den kaçar tane satış gerçekleşmiş?
df["ConceptName"].value_counts()

# Soru5:Şehirlere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("SaleCityName").agg({"Price" : "sum"})

#Soru6:Concept türlerine göre göre ne kadar kazanılmış?
df.groupby("ConceptName").agg({"Price" : "sum"})

#Soru7:Şehirlere göre PRICE ortalamaları nedir?
df.groupby("SaleCityName").agg({"Price" : "mean"})

# Soru8:Conceptlere göre PRICE ortalamaları nedir?
df.groupby("ConceptName")["Price"].mean()

# Soru9:Şehir-Concept kırılımında PRICE ortalamaları nedir?
df.groupby(["ConceptName","SaleCityName"])["Price"].mean()


# Görev 2: SaleCheckInDay Diffdeğişkenini kategorik bir değişkene çeviriniz.

bins = [-1, 7, 30, 90, df["SaleCheckInDayDiff"].max()]
labels = [ "Last Minuters", "Potential Planners", "Planners",  "Early Bookers"]

df["EB_score"] = pd.cut(df["SaleCheckInDayDiff"], bins = bins,labels=labels)
df.head(50).to_excel("eb_scorew.xlsx", index=False)

#Görev 3:  COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
#  Şehir-Concept-EB Score, Şehir-Concept-Sezon, Şehir-Concept-CInDay kırılımında ortalama ödenen ücret ve yapılan işlem sayısı cinsinden
#  inceleyiniz ?

df.groupby(["SaleCityName", "ConceptName", "EB_score"]).agg({"Price" : ["mean","count"]})

df.groupby(["SaleCityName", "ConceptName", "Seasons"]).agg({"Price" : ["mean","count"]})
df.columns

df.groupby(["SaleCityName", "ConceptName", "CInDay"]).agg({"Price" :["mean","count"]})
df["SaleCityName"]



#Görev 4:  City-Concept-Season kırılımının çıktısını PRICE'a göre sıralayınız.

agg_df = df.groupby(["SaleCityName", "ConceptName", "Seasons"]).agg({"Price" : "mean"}).sort_values("Price",ascending = False)
agg_df.head(20)


#Görev 5:  Indekste yer alan isimleri değişken ismine çeviriniz.
#  Üçüncü sorunun çıktısında yer alan PRICE dışındaki tüm değişkenler index isimleridir. Bu isimleri değişken isimlerine çeviriniz.

agg_df.reset_index(inplace = True)

agg_df.head()


#Görev 6:  Yeni seviye tabanlı müşterileri (persona) tanımlayınız.
"""Yeni seviye tabanlı satışları tanımlayınız ve veri setine değişken olarak ekleyiniz.
 • Yeni eklenecek değişkenin adı: sales_level_based
 • Önceki soruda elde edeceğiniz çıktıdaki gözlemleri bir araya getirerek sales_level_baseddeğişkenini oluşturmanız gerekmektedir."""

agg_df['sales_level_based'] = agg_df[["SaleCityName", "ConceptName", "Seasons"]].agg(lambda x: '_'.join(x).upper(), axis= 1)


#############################################
# GÖREV 7: Personaları segmentlere ayırınız.
#############################################
# PRICE'a göre 4 segmentlere ayırınız,
# segmentleri "SEGMENT" isimlendirmesi ile agg_df'e ekleyiniz
# segmentleri betimleyiniz  • Segmentleri betimleyiniz (Segmentlere göre group by yapıp price mean, max, sum’larını alınız).

agg_df["SEGMENT"] = pd.qcut(agg_df["Price"],4, labels= ["D","C","B","A"])
agg_df.head(30)

agg_df.groupby("SEGMENT").agg({"Price" : ["mean", "max", "sum"]})


#Görev 8:  Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini  tahmin ediniz.
""" Antalya’da herşey dahil ve yüksek sezonda tatil yapmak isteyen bir kişinin ortalama ne kadar gelir kazandırması beklenir?
 • Girne’de yarım pansiyon bir otele düşük sezonda giden bir tatilci hangi segmentte yer alacaktır?"""

new_user = "ANTALYA_HERŞEY DAHIL_HIGH"
agg_df[agg_df["sales_level_based"] == new_user]

new_user2 = "GIRNE_YARIM PANSIYON_LOW"
agg_df[agg_df["sales_level_based"] == new_user2]
