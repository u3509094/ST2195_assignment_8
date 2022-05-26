import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

titanic = pd.read_csv("titanic.csv")
titanic.head()
titanic.info()

#Data Pre-processing
titanic.loc[titanic["Survived"] == 0, "Survived"] = "0"
titanic.loc[titanic["Survived"] == 1, "Survived"] = "1"
titanic.loc[titanic["Pclass"] == 1, "Pclass"] = "1"
titanic.loc[titanic["Pclass"] == 2, "Pclass"] = "2"
titanic.loc[titanic["Pclass"] == 3, "Pclass"] = "3"
titanic["Familysize"] = titanic["SibSp"] + titanic["Parch"]

#Q1
sex_count = titanic["Sex"].value_counts().reset_index()
fig, ax = plt.subplots()
ax.bar(sex_count["index"], sex_count["Sex"])
ax.set_xticklabels(["Male", "Female"])
ax.set_xlabel("Gender")
ax.set_ylabel("Count")
ax.set_title("Distribution of Passengers by Gender")
ax.set_ylim(0, 650)
plt.show()

pclass_count = titanic["Pclass"].value_counts().reset_index().sort_values("index")
fig, ax = plt.subplots()
ax.bar(pclass_count["index"], pclass_count["Pclass"])
ax.set_xlabel("Ticket Class")
ax.set_ylabel("Count")
ax.set_title("Distribution of Passengers by Ticket Class")
ax.set_ylim(0, 550)
plt.show()

survived_count = titanic["Survived"].value_counts().reset_index()
fig, ax = plt.subplots()
ax.bar(survived_count["index"], survived_count["Survived"])
ax.set_xlabel("Survival Status")
ax.set_ylabel("Count")
ax.set_title("Distribution of Passengers by Survival Status")
ax.set_ylim(0, 600)
plt.show()

#Q2
fig, ax = plt.subplots()
ax.hist(titanic["Age"])
ax.set_xlabel("Age")
ax.set_ylabel("Count")
ax.set_title("Distribution of Passengers by Age")
ax.set_ylim(0, 200)
plt.show()

Pclass = [titanic.loc[titanic["Pclass"] == "1"]["Age"].dropna(),
          titanic.loc[titanic["Pclass"] == "2"]["Age"].dropna(),
          titanic.loc[titanic["Pclass"] == "3"]["Age"].dropna()]
fig, ax = plt.subplots()
ax.boxplot(Pclass)
ax.set_xlabel("Ticket Class")
ax.set_ylabel("Age")
ax.set_title("Distribution of Passengers by Ticket Class and Age")
plt.show()

Survived = [titanic.loc[titanic["Survived"] == "0"]["Age"].dropna(),
            titanic.loc[titanic["Survived"] == "1"]["Age"].dropna()]
fig, ax = plt.subplots()
ax.boxplot(Survived)
ax.set_xticklabels(["0", "1"])
ax.set_xlabel("Survival Status")
ax.set_ylabel("Age")
ax.set_title("Distribution of Passengers by Survival Status and Age")
plt.show()

#Q3
fig, ax = plt.subplots()
ax.hist(titanic["Fare"], bins = 25)
ax.set_xlabel("Travel Fare")
ax.set_ylabel("Count")
ax.set_title("Distribution of Passengers by Travel Fare")
ax.set_ylim(0, 550)
plt.show()

titanic.loc[titanic["Fare"] == 0]

#Q4
Pclass_Familysize = [titanic.loc[titanic["Pclass"] == "1"].value_counts("Familysize").reset_index().sort_values("Familysize"),
                     titanic.loc[titanic["Pclass"] == "2"].value_counts("Familysize").reset_index().sort_values("Familysize"),
                     titanic.loc[titanic["Pclass"] == "3"].value_counts("Familysize").reset_index().sort_values("Familysize")]
fig, ax = plt.subplots()
patches, texts = ax.pie(Pclass_Familysize[0][0], startangle = 90)
ax.set_title("Distribution of Family Size in 1st Class")
ax.legend(patches, [r'0 (50.5%)', r'1 (32.4%)', r'2 (11.1%)', r'3 (3.2%)', r'4 (0.9%)', r'5 (1.9%)'], title = "Family Size", loc= "center left")
plt.show()

fig, ax = plt.subplots()
patches, texts = ax.pie(Pclass_Familysize[1][0], startangle = 90)
ax.set_title("Distribution of Family Size in 2nd Class")
ax.legend(patches, [r'0 (56.5%)', r'1 (18.5%)', r'2 (16.8%)', r'3 (7.1%)', r'4 (0.5%)', r'5 (0.5%)'], title = "Family Size", loc= "center left")
plt.show()

fig, ax = plt.subplots()
patches, texts = ax.pie(Pclass_Familysize[2][0], startangle = 90)
ax.set_title("Distribution of Family Size in 3rd Class")
ax.legend(patches, [r'0 (66.0%)', r'1 (11.6%)', r'2 (9.6%)', r'3 (1.8%)', r'4 (2.4%)', r'5 (3.4%)', r'6 (2.4%)', r'7 (1.2%)', r'10 (1.4%)'], title = "Family Size", loc= "center left")
plt.show()

#Q5
#Sex vs. Survived
Sex_Survived = [titanic.loc[titanic["Sex"] == "female"].value_counts("Survived").reset_index().sort_values("Survived"),
                titanic.loc[titanic["Sex"] == "male"].value_counts("Survived").reset_index().sort_values("Survived")]
fig, ax = plt.subplots()
ax.bar(Sex_Survived[0]["Survived"], Sex_Survived[0][0], label = "Female")
ax.bar(Sex_Survived[1]["Survived"], Sex_Survived[1][0], bottom = Sex_Survived[0][0], label = "Male")
ax.set_xlabel("Survival Status")
ax.set_ylabel("Count")
ax.set_title("Distribution of Passengers by Survival Status and Gender")
ax.set_ylim(0, 650)
ax.legend()
plt.show()

Sex_Survived = [titanic.loc[titanic["Survived"] == "0"].value_counts("Sex").reset_index().sort_values("Sex"),
                titanic.loc[titanic["Survived"] == "1"].value_counts("Sex").reset_index().sort_values("Sex")]
fig, ax = plt.subplots()
ax.bar(Sex_Survived[0]["Sex"], Sex_Survived[0][0], label = "0")
ax.bar(Sex_Survived[1]["Sex"], Sex_Survived[1][0], bottom = Sex_Survived[0][0], label = "1")
ax.set_xticklabels(["Female", "Male"])
ax.set_xlabel("Gender")
ax.set_ylabel("Count")
ax.set_title("Distribution of Passengers by Gender and Survival Status")
ax.set_ylim(0, 650)
ax.legend()
plt.show()

#Pclass vs. Survived
Pclass_Survived = [titanic.loc[titanic["Pclass"] == "1"].value_counts("Survived").reset_index().sort_values("Survived").reset_index(drop = True),
                   titanic.loc[titanic["Pclass"] == "2"].value_counts("Survived").reset_index().sort_values("Survived").reset_index(drop = True),
                   titanic.loc[titanic["Pclass"] == "3"].value_counts("Survived").reset_index().sort_values("Survived").reset_index(drop = True)]
fig, ax = plt.subplots()
ax.bar(Pclass_Survived[0]["Survived"], Pclass_Survived[0][0], label = "1")
ax.bar(Pclass_Survived[1]["Survived"], Pclass_Survived[1][0], bottom = Pclass_Survived[0][0], label = "2")
ax.bar(Pclass_Survived[2]["Survived"], Pclass_Survived[2][0], bottom = Pclass_Survived[0][0] + Pclass_Survived[1][0], label = "3")
ax.set_xlabel("Survival Status")
ax.set_ylabel("Count")
ax.set_title("Distribution of Passengers by Survival Status and Ticket Class")
ax.set_ylim(0, 600)
ax.legend()
plt.show()

Pclass_Survived = [titanic.loc[titanic["Survived"] == "0"].value_counts("Pclass").reset_index().sort_values("Pclass").reset_index(drop = True),
                   titanic.loc[titanic["Survived"] == "1"].value_counts("Pclass").reset_index().sort_values("Pclass").reset_index(drop = True)]
fig, ax = plt.subplots()
ax.bar(Pclass_Survived[0]["Pclass"], Pclass_Survived[0][0], label = "0")
ax.bar(Pclass_Survived[1]["Pclass"], Pclass_Survived[1][0], bottom = Pclass_Survived[0][0], label = "1")
ax.set_xlabel("Ticket Class")
ax.set_ylabel("Count")
ax.set_title("Distribution of Passengers by Ticket Class and Survival Status")
ax.set_ylim(0, 550)
ax.legend()
plt.show()

#Q6
Age_Survived = [titanic.loc[titanic["Survived"] == "0"]["Age"].dropna(),
                titanic.loc[titanic["Survived"] == "1"]["Age"].dropna()]
fig, ax = plt.subplots()
ax.violinplot([Age_Survived[0], Age_Survived[1]])
ax.set_xlabel("Survival Status")
ax.set_ylabel("Age")
ax.set_xticks([1, 2], labels = ["0", "1"])
ax.set_title("Distribution of Passengers by Survival Status and Age")
plt.show()

ax = sns.violinplot(x = "Survived", y = "Age", hue = "Sex", data = titanic, split = True)
ax.set_xlabel("Survival Status")
ax.set_ylabel("Age")
ax.set_title("Distribution of Passengers \n by Survival Status, Age and Gender")

#Q7
ax = sns.violinplot(x = "Survived", y = "Age", hue = "Pclass", data = titanic)
ax.set_xlabel("Survival Status")
ax.set_ylabel("Age")
ax.legend(title = "Ticket Class")
ax.set_title("Distribution of Passengers \n by Survival Status, Age and Ticket Class")