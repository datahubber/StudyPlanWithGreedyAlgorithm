import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cbook import boxplot_stats
import warnings
warnings.filterwarnings('ignore')

class dataPreprocessing:
	def __init__(self):
		self.data = self.load_data()
		self.skills = [ "Python", "spark", "aws", "excel", "sql", "sas", "keras", "pytorch", "scikit", "tensor", "hadoop", "tableau", "bi", "flink", "mongo", "google_an"]
		self.roles= ["data scientist", "data engineer", "analyst", "machine learning engineer"]
		self.skill_times= pd.read_csv("data/Courses_Level_Hours.csv")


	def func(self,x,i,q1, med,q3):
		'''
		func: lambda function that gives the level for the jobs
		'''
		if x<float(q1):
			return i + " 1"
		elif x<med:
			return i +" 2"
		else:
			return i + " 3"


	def load_data(self):
		'''
		load_data: reads the data, drop na and gets only get the wanted job titles
		'''
		data = pd.read_csv("data/salary_data_raw.csv")[[ "Avg Salary(K)","job_title_sim", "Job Title","Python", "spark", "aws", "excel", "sql", "sas", "keras", "pytorch", "scikit", "tensor", "hadoop", "tableau", "bi", "flink", "mongo", "google_an"]]
		data=data[(data["job_title_sim"] !="na") & (data["job_title_sim"] != "other scientist")]
		data=data.rename(columns={"Avg Salary(K)": "salary"})
		return data


	def levels(self):
		'''
		levels: creates a pandas data frame with job titles with new level and the required skills needed
		'''
		df = pd.DataFrame()
		salary_list=[]

		#uses the apply function and box plot_stats to create new title's based on salary
		for i in self.roles:
			temp_data = self.data[self.data["job_title_sim"]==i]
			stats = boxplot_stats(temp_data['salary'])
			temp_data['adjJobtitle']= temp_data['salary'].apply(lambda x: self.func(x,i,stats[0]["q1"],stats[0]["med"], stats[0]["q3"]))
			salary_list.append(temp_data)
			
			#Appends to data frame
			if df.empty:
				df=temp_data
			else:
				df=df.append(temp_data)
		df.drop("salary", axis=1, inplace=True)
		


		#Finds the sum of all of the times that a skill is needed for each of the differet title 
		#and then multiplies it by the level. This is then rounded and slightly adjusted. 
		df_list = []
		for i in np.unique(df["adjJobtitle"]):
			level = int(i[-1])
			temp = df[df["adjJobtitle"]==i]
			temp.drop(["job_title_sim","Job Title"], axis =1, inplace=True)
			percentageSkillsNeeded= round(0.5+level*temp.loc[:, temp.columns != "adjJobtitle"].sum(axis=0)/len(temp))
			skill_list = [i] +list(percentageSkillsNeeded)
			df_list.append(skill_list)
		requirements_df= pd.DataFrame(df_list, columns=["Job Title"]+self.skills)
		self.data = requirements_df
		self.roles= self.data["Job Title"]
		
		
		
	def get_priorities(self, jobTitle):
		'''
		get_priorities:
		'''
		base_importance = { "Python": 200, "spark": 50, "aws": 50, "excel": 25, "sql": 100, 'sas':30, "keras": 35, "pytorch": 50, "scikit": 55, "tensor": 60, "hadoop":75, "tableau":50, "bi": 60,"flink":40, "mongo": 50, "google_an": 30}
		titleTimes = self.data[self.data["Job Title"]==jobTitle]
		titleTimes=titleTimes.loc[:, (titleTimes.sum(axis=0) != 0)]
		skillsRequired={i: int(titleTimes[i]) for i in titleTimes.columns[1:]}
		
		classes_list=[]
		for s in skillsRequired.keys():
			level=skillsRequired[s]
			if level ==1:
				classes_list.append({"course":s,"level": 1,'hours':40, 'value':base_importance[s], "extra": False})
				classes_list.append({"course":s, "level":2,'hours':50,'value': base_importance[s]*0.4, "extra": True })
				classes_list.append({"course":s, "level":3,'hours':60, 'value':base_importance[s]*0.2, "extra": True})
			if level==2:
				classes_list.append({"course":s,"level": 1,'hours':40, 'value':base_importance[s], "extra": False})
				classes_list.append({"course":s,"level": 2,'hours':50, 'value':base_importance[s]*0.9, "extra": False})
				classes_list.append({"course":s, "level":3,'hours':60, 'value':base_importance[s]*0.2, "extra": True})
			if level==3:
				classes_list.append({"course":s,"level": 1,'hours':40, 'value':base_importance[s], "extra": False})
				classes_list.append({"course":s, "level":2,'hours':50, 'value':base_importance[s]*0.9, "extra": False})
				classes_list.append({"course":s, "level":3,'hours':60, 'value':base_importance[s]*0.8, "extra": False})
				

		return classes_list
				
		
def main(jobTitle="analyst 1",csv=False):
	d = dataPreprocessing()
	d.levels()
	d.get_priorities(jobTitle)
	


if __name__ == "__main__":
	main(jobTitle="analyst 1",csv=False)










