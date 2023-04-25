import heapq
import pprint as pp
from dataPreprocessing import dataPreprocessing
import numpy as np
import pandas as pd
import os

class CourseValue:
	def __init__(self, course_dict):
		self.course = course_dict["course"]
		self.level = course_dict["level"]
		self.hours = course_dict["hours"]
		self.value = course_dict["value"]
		self.extra = course_dict["extra"]
		self.hour_value_ratio = self.value / self.hours

	def __lt__(self, other):
		return self.hour_value_ratio > other.hour_value_ratio

class CourseLevel:
	def __init__(self, course_dict):
		self.course = course_dict["course"]
		self.level = course_dict["level"]
		self.hours = course_dict["hours"]
		self.value = course_dict["value"]
		self.extra = course_dict["extra"]

		self.hour_value_ratio = self.value / self.hours
	def __lt__(self, other):
		return self.level < other.level

def get_course_schedule(courses, total_hours, interviewee_proficiency):
	result = []
	course_heap_dict = {}
	total_value_possible = 0

	# This for loop is taking O(n) where n is len courses list of dict
	for course in courses:
		if course["extra"]==False:
			total_value_possible += course["value"]
		if course["course"] in course_heap_dict.keys():
			course_heap_dict[course["course"]].append(CourseLevel(course))
		else:
			course_heap_dict[course["course"]] = [CourseLevel(course)]

	 # This loop takes O(m*log(l)) m: number of courses, l: max level of course
	course_heap = []
	for course_name, heap in course_heap_dict.items():
		heapq.heapify(heap)
		course = heapq.heappop(heap)
		while interviewee_proficiency[course_name] >= course.level:
			if len(heap) == 0:
				course = None
				break
			course = heapq.heappop(heap)
		if course is not None:
			course_heap.append(CourseValue({"course":course.course, "level":course.level, "hours":course.hours, "value":course.value, "extra": course.extra}))

	heapq.heapify(course_heap)
	num_course_level = len(courses)
	hours_invested = 0
	max_value_acquired = 0
	# this loop takes O(2*n*log(m))
	while hours_invested < total_hours and num_course_level>0:
		max_value_course = heapq.heappop(course_heap)
		time_left_for_interview = total_hours - hours_invested
		if max_value_course.hours >= time_left_for_interview:
			#course_value_acquired = max_value_course.value * time_left_for_interview / course.hours
			hours_invested += time_left_for_interview
			max_value_acquired += round((time_left_for_interview / course.hours)*max_value_course.value, 2)
			course_taken_dict = {
				"course":max_value_course.course,
				"level":max_value_course.level,
				"hours_invested": time_left_for_interview,
				"pcnt_course_value_acquired": round((time_left_for_interview / course.hours)*100, 2),
				"extra": max_value_course.extra
			}
		else:
			hours_invested += max_value_course.hours
			max_value_acquired += max_value_course.value
			course_taken_dict = {
				"course":max_value_course.course,
				"level":max_value_course.level,
				"hours_invested": max_value_course.hours,
				"pcnt_course_value_acquired": 100,
				"extra": max_value_course.extra
			}
		result.append(course_taken_dict)
		num_course_level -= 1
		if	len(course_heap_dict[max_value_course.course]) > 0:
			course = heapq.heappop(course_heap_dict[max_value_course.course])
			heapq.heappush(course_heap, CourseValue({"course":course.course, "level":course.level, "hours":course.hours, "value":course.value, "extra": course.extra}))
	pcnt_preparation = (max_value_acquired / total_value_possible)*100
	return result, pcnt_preparation


# Total Time Complexity = O(n +mlog(l) + nlog(m)) = O(nlog(m))
# Space Complexity = O(n)

if __name__ == "__main__":

	##### Preprocesses the data
	d=dataPreprocessing()
	d.levels()
	skills = d.skills
	job_data=d.data
	course_data = d.skill_times



	####user input 
	print("Please choose a role from the following list:")
	for role in d.roles:
		print(role)
		
		
		
	###The code below can be commented/uncommented out if you want to make this more interactive.
 	#chosen_role = "analyst 1"
 	#total_hrs = 1000
	chosen_role = input("\nEnter the role you are interested in: ")
	total_hrs = int(input("Enter the number of preparation hours: "))

	####Generates value for each class with built in priorities basesd off of user input or precoded 0's for all required skills
	courses = sorted(d.get_priorities(chosen_role), key=lambda x: x["value"], reverse=True)
	courses_df= pd.DataFrame(courses, columns=["course", "level", "hours", "value", "extra"])
	unique_courses=np.unique(courses_df["course"])
	interviewee_proficiency={}
	for i in unique_courses:
		interviewee_proficiency[i]=0
		
		###The code below can be uncommented out if you want to make this more interactive.
 		#proficiency =input(f"On a scale of 0-3 how proficient are you at {i} ")
 		#if (int(proficiency)>3) or (int(proficiency)<0):
 		#	proficiency =input(f"Try again. On a scale of 0-3 how proficient are you at {i} ")
 		#interviewee_proficiency[i]=proficiency
	
	###Cleans system
	os.system('cls' if os.name == 'nt' else 'clear')


	#Prints the final screen
	print("Plan for the interview looks like below(time in hrs):")
	print(f'\nThese are the classes you need to take in order: \n')
	study_plan, pcnt_preparation = get_course_schedule(courses, total_hrs, interviewee_proficiency)
	required_courses = [course["course"]+ " " + str(course["level"])+" : "+ str(course["hours_invested"]) +"(h)" for course in study_plan if course["extra"]==False ]
	for i in required_courses:
		print(i)
		
	#Prints info about the extra courses
	if pcnt_preparation>100:
			extra_courses = [course["course"]+ " " + str(course["level"]) for course in study_plan if course["extra"]==True ]
			print(f"\nPercentage chance to crack the interview with {total_hrs} hours with the plan is: 100%")
			print("\nYou even prepaired extra by taking these classes: \n")
			for i in extra_courses:
				print(i)
	else:
		print(f"\nPercentage chance to crack the interview with {total_hrs} hours with the plan is: {pcnt_total_value_acquired}%")


	###Uncomment this out if you want to keep the old way of output
 	#pp.pprint(study_plan)

	



