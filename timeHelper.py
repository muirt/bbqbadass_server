import datetime

def time_list(timestamp):
      t_list = []


      #expecting string to be in format: 2016-03-11 03:02:33.633609,
      #as produced by datetime
      YEAR_ELEMENT = 0
      MONTH_ELEMENT = 1
      DAY_ELEMENT = 2
      HOUR_ELEMENT = 0
      MINUTE_ELEMENT = 1
      SECOND_ELEMENT = 2

      timestamp_elements = timestamp.split(" ")
      date_str = timestamp_elements[0]
      time_str = timestamp_elements[1]

      date_elements = date_str.split("-")
      time_elements = time_str.split(":")
      time_elements[SECOND_ELEMENT] = time_elements[SECOND_ELEMENT].split(".")[0]

      t_list.append(date_elements[YEAR_ELEMENT])  
      t_list.append(date_elements[MONTH_ELEMENT])
      t_list.append(date_elements[DAY_ELEMENT])

      t_list.append(time_elements[HOUR_ELEMENT])
      t_list.append(time_elements[MINUTE_ELEMENT])
      t_list.append(time_elements[SECOND_ELEMENT])

      return t_list
      
def get_time_difference( str1, str2):

      time_1 = time_list(str1)
      time_2 = time_list(str2)

      datetime_1 = datetime.datetime(int(time_1[0]), int(time_1[1]), int(time_1[2]), int(time_1[3]), int(time_1[4]), int(time_1[5]))
      datetime_2 = datetime.datetime(int(time_2[0]), int(time_2[1]), int(time_2[2]), int(time_2[3]), int(time_2[4]), int(time_2[5]))     
      diff = (datetime_1 - datetime_2).total_seconds()    
      
      return diff