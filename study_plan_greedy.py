import pprint as pp

class StudyPlanBasic:
    def greedy_algo(self, course_list, time_left_for_interview):
        # sorting courses by value to hours ratio
        course_list.sort(key=lambda course: (course["value"]/course["hours"]), reverse=True)
        max_possible_value = 0
        for course in course_list:
            max_possible_value += course["value"]
        value_acquired = 0
        courses_taken = []
        # Looping through all Items
        for course in course_list:
            # If adding course won't exhaust all the time
            # add all the hours of the course
            if course["hours"] <= time_left_for_interview:
                time_left_for_interview -= course["hours"]
                value_acquired += course["value"]
                courses_taken.append(
                    {
                        "course": course["subject"],
                        "percentage_value_acquired": round((course["value"]/course["value"])*100, 2),
                        "time_spend": course["hours"]
                    })
            # If we can't take the whole course,
            # just spend the fractional time
            else:
                course_value_acquired = course["value"] * time_left_for_interview / course["hours"]
                value_acquired += course_value_acquired
                courses_taken.append(
                    {
                        "course": course["subject"],
                        "percentage_value_acquired": round((course_value_acquired/course["value"])*100, 2),
                        "time_spend":time_left_for_interview
                    })
                break
        # Returning final value
        percentage_value_acquired = round((value_acquired/max_possible_value) * 100, 2)
        return courses_taken, percentage_value_acquired


if __name__ == "__main__":
    plan = StudyPlanBasic()
    courses = [
		{
			"subject": "AWS",
			"hours": 50,
			"value": 30
		},
		{
			"subject": "Python",
			"hours": 60,
			"value": 80
		},
		{
			"subject": "ML",
			"hours": 50,
			"value": 80
		},
		{
			"subject": "SQL",
			"hours": 30,
			"value": 30
		},
	]
    total_hrs = 120
    study_plan, pcnt_total_value_acquired = plan.greedy_algo(courses, total_hrs)
    print("Plan for the interview looks like below(time in hrs):")
    pp.pprint(study_plan)
    print(f"Percentage chance to crack the interview with {total_hrs}\
 hours with the plan is: {pcnt_total_value_acquired}%")
