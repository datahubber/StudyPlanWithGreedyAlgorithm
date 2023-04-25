import pandas as pd
import pprint as pp
from dataPreprocessing import dataPreprocessing

class StudyPlanBasic:
	def dp_algo(self, course_list, time_left_for_interview, index=0, memo=None):
		if memo is None:
			memo = {}
		if index == len(course_list):
			return [], 0
		if (time_left_for_interview, index) in memo:
			return memo[(time_left_for_interview, index)]

		courses_taken_skip, value_acquired_skip = self.dp_algo(course_list, time_left_for_interview, index + 1, memo)

		course = course_list[index]
		if course["hours"] <= time_left_for_interview:
			courses_taken_take, value_acquired_take = self.dp_algo(
				course_list, time_left_for_interview - course["hours"], index + 1, memo
			)
			value_acquired_take += course["value"]
			courses_taken_take.append(
				{
					"course": course["course"],
					"level": course["level"],
					"percentage_value_acquired": round((value_acquired_take / course["value"]) * 100, 2) if course["value"] != 0 else 0,
					"time_spend": course["hours"],
					"extra": course ["extra"]
				})

			memo[(time_left_for_interview, index)] = courses_taken_take, value_acquired_take
		else:
			fraction = time_left_for_interview / course["hours"]
			value_acquired_fraction = course["value"] * fraction
			courses_taken_fraction = [
				{
					"course": course["course"],
					"level": course["level"],
					"percentage_value_acquired": round((value_acquired_fraction / course["value"]) * 100, 2) if course["value"] != 0 else 0,
					"time_spend": time_left_for_interview,
					"extra": course ["extra"]
				}]
			memo[(time_left_for_interview, index)] = courses_taken_fraction, value_acquired_fraction

		if memo[(time_left_for_interview, index)][1] < value_acquired_skip:
			memo[(time_left_for_interview, index)] = courses_taken_skip, value_acquired_skip

		return memo[(time_left_for_interview, index)]
if __name__ == "__main__":

	d=dataPreprocessing()
	d.levels()
	skills = d.skills
	job_data=d.data
	course_data = d.skill_times

	print("Please choose a role from the following list:")
	for role in d.roles:
		print(role)

	chosen_role = input("Enter the role you are interested in: ")
	total_hrs = int(input("Enter the number of preparation hours: "))
	relevant_courses = sorted(d.get_priorities(chosen_role), key=lambda x: x["value"], reverse=True)

	plan = StudyPlanBasic()

	study_plan, value_acquired = plan.dp_algo(relevant_courses, total_hrs)
	
	
	
	max_possible_value = sum(course["value"] for course in relevant_courses if course["extra"]==False )
	pcnt_total_value_acquired = round((value_acquired / max_possible_value) * 100, 2) if max_possible_value != 0 else 0

	print("Plan for the interview looks like below(time in hrs):")
	study_plan = [course for course in study_plan if course["time_spend"] > 0]
	study_plan = sorted(study_plan, key=lambda x: (x["percentage_value_acquired"], x["level"]), reverse=True)
	pp.pprint(study_plan)
	if pcnt_total_value_acquired>100:
		extra_courses = [course["course"]+ " " + str(course["level"]) for course in study_plan if course["extra"]==True ]
		print(f"Percentage chance to crack the interview with {total_hrs} hours with the plan is: 100%")
		print(f"\nYou even prepaired extra by taking these classes: \n {extra_courses} ")
	else:
		print(f"Percentage chance to crack the interview with {total_hrs} hours with the plan is: {pcnt_total_value_acquired}%")
	
	
	
	
	
	
	
	