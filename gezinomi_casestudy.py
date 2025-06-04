import pandas as pd
import numpy as np

df = pd.read_excel("miuul_gezinomi.xlsx")
df.head()
pd.set_option('display.max_columns', None)
pd.set_option('display.width',500)

# Question2:How many unique cities are there? What are their frequencies?
df["SaleCityName"].unique()
df["SaleCityName"].value_counts()

# Question 3: How many unique Concepts are there?
df["ConceptName"].nunique()

# Question 4: How many sales were made from which Concept?
df["ConceptName"].value_counts()

# Question 5: How much total was earned from sales by city?
df.groupby("SaleCityName").agg({"Price" : "sum"})

# Question 6: How much was earned according to concept types?
df.groupby("ConceptName").agg({"Price" : "sum"})

# Question 7: What are the PRICE averages by city?
df.groupby("SaleCityName").agg({"Price" : "mean"})

# Question 8: What are the PRICE averages according to concepts?
df.groupby("ConceptName")["Price"].mean()

# Question 9: What are the PRICE averages in the City-Concept breakdown?
df.groupby(["ConceptName","SaleCityName"])["Price"].mean()


# Task 2: Convert the SaleCheckInDay Diff variable to a categorical variable.

bins = [-1, 7, 30, 90, df["SaleCheckInDayDiff"].max()]
labels = [ "Last Minuters", "Potential Planners", "Planners",  "Early Bookers"]

df["EB_score"] = pd.cut(df["SaleCheckInDayDiff"], bins = bins,labels=labels)
df.head(50).to_excel("eb_scorew.xlsx", index=False)

# Task 3:  What are the average earnings in COUNTRY, SOURCE, SEX, AGE breakdown?
# Examine the City-Concept-EB Score, City-Concept-Season, City-Concept-CInDay breakdown in terms of average paid wage and number of transactions made

df.groupby(["SaleCityName", "ConceptName", "EB_score"]).agg({"Price" : ["mean","count"]})

df.groupby(["SaleCityName", "ConceptName", "Seasons"]).agg({"Price" : ["mean","count"]})
df.columns

df.groupby(["SaleCityName", "ConceptName", "CInDay"]).agg({"Price" :["mean","count"]})
df["SaleCityName"]



# Task 4: Sort the output of the City-Concept-Season breakdown by PRICE.

agg_df = df.groupby(["SaleCityName", "ConceptName", "Seasons"]).agg({"Price" : "mean"}).sort_values("Price",ascending = False)
agg_df.head(20)


# Task 5: Convert the names in the index to variable names.
# All variables except PRICE in the output of the third question are index names. Convert these names to variable names.

agg_df.reset_index(inplace = True)

agg_df.head()


# Task 6: Define new level-based customers (personas).
"""Define new level-based sales and add it to the data set as a variable.
• The name of the new variable to be added: sales_level_based
• You need to create the sales_level_based variable by bringing together the observations in the output you will obtain in the previous question."""

agg_df['sales_level_based'] = agg_df[["SaleCityName", "ConceptName", "Seasons"]].agg(lambda x: '_'.join(x).upper(), axis= 1)


#############################################
# TASK 7: Segment the personas.
###########################################
# Segment into 4 segments according to PRICE,
# Add the segments to agg_df with the name "SEGMENT"
# Describe the segments • Describe the segments (Group by segments and get the price mean, max, sum).

agg_df["SEGMENT"] = pd.qcut(agg_df["Price"],4, labels= ["D","C","B","A"])
agg_df.head(30)

agg_df.groupby("SEGMENT").agg({"Price" : ["mean", "max", "sum"]})


# Task 8: Classify new customers and estimate how much revenue they can bring.
""" Antalya’da herşey dahil ve yüksek sezonda tatil yapmak isteyen bir kişinin ortalama ne kadar gelir kazandırması beklenir?
 • Girne’de yarım pansiyon bir otele düşük sezonda giden bir tatilci hangi segmentte yer alacaktır?"""

new_user = "ANTALYA_HERŞEY DAHIL_HIGH"
agg_df[agg_df["sales_level_based"] == new_user]

new_user2 = "GIRNE_YARIM PANSIYON_LOW"
agg_df[agg_df["sales_level_based"] == new_user2]
