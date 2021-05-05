import datetime
def process_day(day):
    switcher = {
         "Saturday":0,
         "Sunday" :1,
         "Monday":2,
         "Tuesday":2,
         "Wednesday":2,
         "Thursday":1,
         "Friday":0
    }
    return switcher.get(day, "ERROR")


#print(process_day('Sunday'))

data = []
with open(r'mohkhali-test-final.txt', 'r') as file:
    # read a list of lines into data
    data = file.readlines()

# for i in range(0, len(data)):
#     tmp = data[i][0:-1]
#     arr = tmp.split(",")
#
#     test = datetime(arr[1])


#    arr[1] = "1"

test = '05022021'
test2 = datetime.datetime(5022021)
print(test2)

print(f'day{test[:2]}--month {test[2:4]}--- year {test[4:]}')
# image = 'G:\SPL3 Repo\SoftwareProjectLab3_GG\ImageToDataPreprocessing\Test Dataset\Mohakhali\Cleaned\Mohakhali_Thursday_04022021_10_10_21.png'
# import base64
# encoded = base64.b64encode(open(image, "rb").read())
# print(str(encoded)[2:-1])