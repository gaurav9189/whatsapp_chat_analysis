import pandas as pd
import regex as re

member = []
date = []
time_stamp = []
with open('_chat.txt', mode='r') as chat:
    # print(chat.readline())
    messages = chat.readlines()
    # print(messages)
    pattern = re.compile(
        r"((^\[\d+.\d+.\d+),\s((\d+.)+[amp]+)\]).([a-zA-Z\d\s]+)")
    for message in messages:
        result = re.match(pattern, message)
        if result:
            member.append(result.group(5))
            date.append(result.group(2))
            time_stamp.append(result.group(3))

            # print(member)

# print(len(time_stamp), len(member), len(date))

df1 = pd.DataFrame(zip(date, time_stamp, member), columns=[
                   'date', 'timestamp', 'member'])
print(df1.head())
print(df1.groupby(['member'], sort=True).count())
# print(df2.head())
# print(df3.head())
# Need to create a function to filter pattern based on time date author and message
