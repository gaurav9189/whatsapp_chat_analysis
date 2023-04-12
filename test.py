import pandas as pd
import regex as re

parse_data = []
msg_buffer = []
# Pattern1 doesn't include unsaved contacts and the media ommitted messages
pattern1 = re.compile(
    r"((^\[\d+.\d+.\d+),\s((\d+.)+[amp]+)\]).([a-zA-Z'\d\s\+]+):(.*)")
# Pattern2 only includes messages starting with letters not with emoji! sad! :(
pattern2 = re.compile(
    r"^([a-zA-Z0-9.*\s%&\$’\_()+^@#\-:]+)")


def clean_message(raw_message):
    message = raw_message.encode('ascii', 'ignore').decode()
    return message


def tokenise(messages, pattern1, pattern2):
    # Initialising variables because we are declaring them late(due to msg buffer)
    date, time_stamp, member = None, None, None
    for raw_message in messages:
        message = clean_message(raw_message)
        result = re.match(pattern1, message)
        if result:
            if len(msg_buffer) > 0:
                parse_data.append(
                    [date, time_stamp, member, ' '.join(msg_buffer)])  # Only appending once messages are reconciled with buffer
            msg_buffer.clear()  # CLearning the buffer once parsed
            # Tokens are populated only once the buffer is added to ensure previous token are used to populate the table
            member = result.group(5)
            date = result.group(2).split('[')[1]
            time_stamp = result.group(3)
            txt = result.group(6)  # used only for appending to buffer
            # declaring other tokens but only creating buffer for texts
            msg_buffer.append(txt)
        else:
            full_message(pattern2, message)


def full_message(pattern2, message):
    complete_msg = re.match(pattern2, message)
    if complete_msg:
        # adds to the msg buffer where ever messages start without author and date
        msg_buffer.append(complete_msg.group(1))
    else:
        print(message)


with open('_chat.txt', mode='r') as chat:
    # print(chat.readline())
    messages = chat.readlines()
    # print(messages)
    tokenise(messages, pattern1, pattern2)

df = pd.DataFrame(parse_data, columns=['data', 'time', 'member', 'message'])
# print(df.head())
# print(df['message'].head())
df.to_csv('chat_clean.txt', sep='\t')
