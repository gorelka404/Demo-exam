import datetime
from fastapi import Body,FastAPI

class Order:
    def __init__(self, number, day, month, year, device, model, problemType, familiya, name, otchestvo, phonenumber, status):
        self.number = number
        self.startDate = datetime(day, month, year)
        self.endDate = None
        self.device = device
        self.model = model
        self.problemType = problemType
        self.fio = (familiya, name, otchestvo)
        self.phonenumber = phonenumber
        self.status = status
        self.comments = []

order = Order(1, 1,1,2099, "webshooter", "homemade", "nopewpew","Цепилов", "Александр", "Андреевич", "+7999-999_00_00", "новая заявка")

isUpdatedStatus = False
message = ""

repo = []
repo.append(order)

app = FastAPI()

@app.get("/")
def get_orders():
    global isUpdatedStatus
    global message
    if(isUpdatedStatus):
        buffer = message
        isUpdatedStatus
        message = ""
        return repo, buffer
    else:
       return repo

@app.post("/")
def create_orders(data = Body()):
    order = Order(
        data["number"],
        data["day"],
        data["month"],
        data["year"],
        data["device"],
        data["model"],
        data["problemType"],
        data["fio"],
        data["status"]
    )
    repo.append(order)
    return order

@app.put("/{number}")
def update_order(number, dto = Body()):
    global isUpdatedStatus
    global message
    isEmpty = True
    for order in repo:
        if order.number == int(number):
            isEmpty = False
            if(order.status != dto["status"]):
                order.status == dto["status"]
                isUpdatedStatus = True
                message += "Статус заявки номер " + str(order.number) + " изменён!"
                if order.status == "завершено":
                    order.endDate == datetime.now()
            if(order.problemType != dto["problemType"]):
                order.problemType == dto["problemType"]
            if(order.master != dto["master"]):
                order.master == dto["master"]
            if (dto["comment"] != None):
                order.comments.append(dto["comment"])
            return order
    if isEmpty:
        return "Ошибка"
    
@app.get("/{num}")
def getByNum(num):
    return [o for o in repo if o.number == int(num)][0]

@app.get("/{param}")
def getByParam(param):
    return [o for o in repo if
            o.device == param or
            o.model == param or
            o.problemType == param or
            o.familiya == param or
            o.name == param or
            o.otchestvo == param or
            o.status == param or
            o.master == param]

@app.get("/stat/completeCount")
def complete_count():
    return len(complete_orders())

@app.get("/stat/problemTypes")
def problem_types():
    result = {}
    for o in repo:
        if o.problemType in result:
            result[o.problemType] += 1
        else:
            result[o.problemType] = 1
    return result

@app.get("/stat/avg")
def avg_time():
    completed = complete_orders()
    times = []
    for o in completed:
        times.append(o.endDate-o.startDate)
    timesSum = sum([t.days for t in times])
    ordCount = complete_count()
    result = timesSum/ordCount
    return result

def complete_orders():
    return [o for o in repo if o.status == "завершено"]