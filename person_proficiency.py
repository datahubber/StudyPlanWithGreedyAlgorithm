class CourseValue:
    def __init__(self, course_dict):
        self.course = course_dict["course"]
        self.level = course_dict["level"]
        self.hours = course_dict["hours"]
        self.value = course_dict["value"]
        self.hour_value_ratio = self.value / self.hours

    def __lt__(self, other):
        return self.hour_value_ratio > other.hour_value_ratio

class CourseLevel:
    def __init__(self, course_dict):
        self.course = course_dict["course"]
        self.level = course_dict["level"]
        self.hours = course_dict["hours"]
        self.value = course_dict["value"]
        self.hour_value_ratio = self.value / self.hours

    def __lt__(self, other):
        return self.level < other.level

def get_course_schedule(courses, total_hours, interviewee_proficiency):
    result = []
    course_heap_dict = {}
    total_value_possible = 0

    # This for loop is taking O(n) where n is len courses list of dict
    for course in courses:
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
            course_heap.append(CourseValue({"course":course.course, "level":course.level, "hours":course.hours, "value":course.value}))

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
                "pcnt_course_value_acquired": round((time_left_for_interview / course.hours)*100, 2)
            }
        else:
            hours_invested += max_value_course.hours
            max_value_acquired += max_value_course.value
            course_taken_dict = {
                "course":max_value_course.course,
                "level":max_value_course.level,
                "hours_invested": max_value_course.hours,
                "pcnt_course_value_acquired": 100
            }
        result.append(course_taken_dict)
        num_course_level -= 1
        if  len(course_heap_dict[max_value_course.course]) > 0:
            course = heapq.heappop(course_heap_dict[max_value_course.course])
            heapq.heappush(course_heap, CourseValue({"course":course.course, "level":course.level, "hours":course.hours, "value":course.value}))
    pcnt_preparation = (max_value_acquired / total_value_possible)*100
    return result, pcnt_preparation


if __name__ == "__main__":
    total_hrs = 250
    courses = [
    {
        "course": "AWS",
        "level": 1,
        "hours": 40,
        "value": 20     # ratio=0.5
    },
    {
        "course": "AWS",
        "level": 2,
        "hours": 50,
        "value": 30    # ratio=0.6
    },
    {
        "course": "AWS",
        "level": 3,
        "hours": 60,
        "value": 150  # ratio=2.5
    },
    {
        "course": "Python",
        "level": 1,
        "hours": 40,
        "value": 100   # ratio=2.5
    },
    {
        "course": "Python",
        "level": 2,
        "hours": 50,
        "value": 240   # ratio=4.8
    },
    {
        "course": "Python",
        "level": 3,
        "hours": 60,
        "value": 20  # ratio=0.33
    },
    {
        "course": "ML",
        "level": 1,
        "hours": 40,
        "value": 180 # ratio=4.5
    },
    {
        "course": "ML",
        "level": 2,
        "hours": 50,
        "value": 200 # ratio=4
    },
    {
        "course": "ML",
        "level": 3,
        "hours": 60,
        "value": 250  # ratio=4.16
    },
    {
        "course": "SQL",
        "level": 1,
        "hours": 40,
        "value": 80    #ratio=2
    },
    {
        "course": "SQL",
        "level": 2,
        "hours": 50,
        "value": 120    #ratio=2.4
    },
    {
        "course": "SQL",
        "level": 3,
        "hours": 60,
        "value": 20  #ratio=0.33
    },

]
    interviewee_proficiency = {
    'Python': 1,
    'AWS': 2,
    'ML':0,
    'SQL': 0
                          }


