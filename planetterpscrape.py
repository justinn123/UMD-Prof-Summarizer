import planetterp
from funcs.rankCourses import rankDep
from funcs.rankProfGpa import *

def rankProf(courseValue):
    try:
        course = planetterp.course(name=courseValue)  
        prof_list = course["professors"]
    except:     
        print(f"Could not find course")
        return
    
    prof_score = []
    for x in prof_list:
        prof = planetterp.professor(name=x)
        if(prof["average_rating"] != None):
            prof_score.append(float('{0:.2f}'.format(prof["average_rating"])))
        else:
            prof_score.append(-1)

    prof_dictionary = dict(zip(prof_list, prof_score))
    ranked = dict(sorted(prof_dictionary.items(), key = lambda item: item[1],reverse = True))
    ranked_str = ""
    counter = 1
    
    for key in ranked:
        if ranked[key] == -1:
            ranked_str+=str(f"{counter}) {key}: None")
        else:
            ranked_str+=str(f"{counter}) {key}: {ranked[key]}")
        ranked_str+=("\n")
        counter+=1
    print(f"{ranked_str}")


def getGPA(courseName, prof):
    average_gpa = calcGPA(courseName, prof)
    if(average_gpa == -1):
        print(f"No Data")
        return
    print(f"Average GPA: {average_gpa:.2f}")


def rankGPA(courseVal):
    list = rankByGPA(courseVal)
    print(list)
    

def rankCourses(department, level):
    list = rankDep(department, level)
    if list:
        print(f"{list}")
    else:
        print(f"There was an error")


def main ():
    rankProf("CMSC433")
    
if __name__ == "__main__":
    main()