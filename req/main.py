import csv
from datetime import datetime

# Получение id пользователя и id класса
user_id, class_id = input().split()

# Получение всех необходимфх данных из файлов
with open("user.csv", "r", encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)
    users = list(reader)
with open("class_user_link.csv", "r", encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)
    class_user_links = list(reader)
with open("test_class_user_link.csv", "r", encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)
    test_class_user_links = list(reader)
with open("test_task_link.csv", "r", encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)
    test_task_links = list(reader)
with open("test_attempt.csv", "r", encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)
    test_attempts = list(reader)
with open("task_attempt.csv", "r", encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)
    task_attempts = list(reader)
with open("test.csv", "r", encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)
    tests = {test[0]: test[1] for test in list(reader)}
with open("task.csv", "r", encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)
    tasks = list(reader)
    
# Получение имени и фамилии пользователя
for link in users:
    if link[0] == user_id:
        user_first_name = link[2]
        user_last_name = link[4]

# Сохранение всех данных о юзере
user = {
    "user.id": user_id,
    "full_name": f"{user_last_name} {user_first_name}",
    "class.id": class_id
}

# Получение информации о всех тестах:
for link in class_user_links:
    if link[1] == class_id and link[2] == user_id:
        class_user_id = link[0]

id_asigned_test = []
test_class_user_linkas = {}

for link in test_class_user_links:
    if link[2] == class_user_id:
        id_asigned_test.append(link[1])
        test_class_user_linkas[link[1]] = link[0]

asigned_test = []
complited_test = 0      

for link in test_class_user_links:
    if link[2] == class_user_id:
        test_id = link[1]
        test_class_user_id = link[0]
        datetime_started = datetime.strptime(link[3], "%d.%m.%Y %H:%M:%S")
            
        test_name = tests.get(test_id, "Unknown test")
            
        for i in test_attempts:
            if i[1] == test_class_user_id:
                if i[2] == "TRUE":
                    flag_is_finished = "TRUE"
                    complited_test += 1
                else:
                    flag_is_finished = "FALSE"
            
        test = {
            "test_name": test_name,
            "datetime_started": datetime_started,
            "flag_is_finished": flag_is_finished
        }

        if len(asigned_test) == 0:
            asigned_test.append(test)
        else:
            for i, link in enumerate(asigned_test[::-1]):
                if test["datetime_started"] > link["datetime_started"]:
                    asigned_test.insert(i, test)
                else:
                    asigned_test.insert(0, test)
                    
progress = {
    "tests_completed": complited_test,
    "tests_total": len(asigned_test),
    "accuracy_average_percent": None
}

# Получение и сохранение всей информации о вопросах в тесте
test_attempt_ids = {}
for i in test_attempts:
    for key, value in test_class_user_linkas.items():
        if i[1] == value:
            test_attempt_ids[key] = i[0]

count_times = {}
progress_percents = {}
correct_percents = {}
count_answers = {}           
correct_answers = {}                  
test_tasks = {}

for test in id_asigned_test:
    count_answers[test] = 0
    correct_answers[test] = 0
    count_time = 0
    test_tasks[test] = []
    for link in test_task_links:
        if link[1] == test:
            task_id = link[2]
            order_number = link[3]
            test_attempt_id = test_attempt_ids.get(test)
            
            user_answer = ""
            time_spent = 0
            correct_answer = ""
            
            for i in task_attempts:
                if i[1] == task_id and i[2] == test_attempt_id:
                    user_answer = i[3]
            
            for i in tasks:
                if i[0] == task_id:
                    correct_answer = i[2]    
                  
            if not user_answer.strip():
                flag_task = "?"
            elif user_answer == correct_answer:
                flag_task = "TRUE"
                correct_answers[test] = correct_answers[test] + 1
                count_answers[test] = count_answers[test] + 1
            else:
                flag_task = "FALSE"
                count_answers[test] = count_answers[test] + 1
                
            for i in task_attempts:
                if task_id == i[1] and i[2] == test_attempt_id:
                    time_spent = int(i[5]) if i[5] else 0
                                    
            data = {
                "order_number": order_number,
                "flag_task": flag_task,
                "task_id": task_id,
            }
            
            count_time += time_spent
            
            test_tasks[test].append(data)
    hours, remainder = divmod(count_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    count_times[test] = time

    if count_answers[test] == 0:
        correct_percents[test] = 0
        progress_percents[test] = 0
    else:
        progress_percents[test] = round(count_answers[test] / len(test_tasks[test]) * 100, 1)
        correct_percents[test] = round(correct_answers[test] / count_answers[test] * 100, 1)
    
test_names = {}
datetimes_assigned = {}

for i in test_tasks:
    test_name = tests.get(i)
    test_names[i] = test_name
    
for i in test_class_user_links:
    for j in test_tasks:
        if i[1] == j:
            datetime_started = i[3]
            datetimes_assigned[j] = datetime_started
            

all_tests = []
date_format = "%d.%m.%Y %H:%M:%S"

for key, value in test_tasks.items():
    tests_dict = {}
    tests_dict["test.id"] = key
    tests_dict["title"] = test_names.get(key)
    tests_dict["tasks"] = []
    
    for index in range(len(value)):
        tests_dict["tasks"].append({})
        tests_dict["tasks"][index]["order_number"] = value[index]["order_number"]
        tests_dict["tasks"][index]["task.id"] = value[index]["task_id"]
        tests_dict["tasks"][index]["is_correct"] = value[index]["flag_task"]
        
    tests_dict["progress_percent"] = round(progress_percents.get(key), 1)
    tests_dict["correct_percent"] = round(correct_percents.get(key), 1)
    tests_dict["time"] = count_times.get(key)
    tests_dict["date_assigned"] = datetimes_assigned.get(key)
    
    if len(all_tests) == 0:
        all_tests.append(tests_dict)
    else:
        for i, link in enumerate(all_tests[::-1]):
            if tests_dict["date_assigned"] > link["date_assigned"]:
                all_tests.insert(i, tests_dict)
            else:
                all_tests.insert(0, tests_dict)
                
for i in all_tests:
    dt = datetime.strptime(i["date_assigned"], "%d.%m.%Y %H:%M:%S")
    new_date_str = dt.strftime("%d.%m.%y")
    i["date_assigned"] = new_date_str

correct_percentas = 0
count_correct_percent = 0

for i in all_tests:
    correct_percentas += i["correct_percent"]
    if i["progress_percent"] != 0:
        count_correct_percent += 1
    
accuracy_average_percent = correct_percentas / count_correct_percent
progress["accuracy_average_percent"] = accuracy_average_percent


data = {
    "user": user,
    "progress": progress,
    "tests": all_tests
}

print("{")
print('  "user": {')
print(f'    "user_id": {int(data["user"]["user.id"])},')
print(f'    "full_name": "{data["user"]["full_name"]}",')
print(f'    "class_id": {int(data["user"]["class.id"])}')
print("  },")

print('  "progress": {')
print(f'    "tests_completed": {data["progress"]["tests_completed"]},')
print(f'    "tests_total": {data["progress"]["tests_total"]},')
print(f'    "accuracy_average_percent": {data["progress"]["accuracy_average_percent"]}')
print("  },")

print('  "tests": [')

for i, test in enumerate(data["tests"]):
    print("    {")
    print(f'      "test_id": {int(test["test.id"])},')
    print(f'      "title": "{test["title"]}",')
    print('      "tasks": [')

    for j, task in enumerate(test["tasks"]):
        print("        {")
        print(f'          "order_number": {int(task["order_number"])},')
        print(f'          "task_id": {int(task["task.id"])},')
        print(f'          "is_correct": "{task["is_correct"]}"')
        
        if j == len(test["tasks"]) - 1:
            print("        }")
        else:
            print("        },")

    print("      ],")
    print(f'      "progress_percent": {float(test["progress_percent"])},')
    print(f'      "correct_percent": {float(test["correct_percent"])},')
    print(f'      "time": "{test["time"]}",')
    print(f'      "date_assigned": "{test["date_assigned"]}"')

    if i == len(data["tests"]) - 1:
        print("    }")
    else:
        print("    },")

print("  ]")
print("}")



        
 


    

        




