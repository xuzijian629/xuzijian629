import fetch_records
import datetime


def to_sec(s):
    return int(s[0]) * 60 + int(s[2:4]) + int(s[5:]) / 1000


wr_data = []
my_data = []

with open('mk8dxwr.txt', 'r') as f:
    for line in f.read().split('\n'):
        wr_data.append(line.split(': '))

with open('record.txt', 'r') as f:
    for line in f.read().split('\n'):
        my_data.append(line.split(': '))

data = []

for i in range(48):
    assert wr_data[i][0] == my_data[i][0]
    data.append((wr_data[i][0], to_sec(wr_data[i][1]), to_sec(
        my_data[i][1]), '' if len(my_data[i]) == 2 else my_data[i][2]))


def to_str(sec):
    sec = int(sec * 1000)
    return '{}\'{:02d}"{:03d}'.format(sec // 1000 // 60, sec // 1000 % 60, sec % 1000)


def make_markdown_table(data):
    ret = '||コース名|自己記録|WRとの差|日付\n'
    ret += '|--|--|--|--|--|\n'
    idx = 1
    for t in data:
        ret += '|{}|{}|{}|+{:.3f}|{}|\n'.format(idx,
                                                t[0], to_str(t[2]), t[2] - t[1], t[3])
        idx += 1
    ret += '\n'
    ret += 'ゴースト: 1101-6752-0152\n\n'
    ret += '全コース8秒落ち: 2020-09-16\n\n'
    ret += '全コース7秒落ち: 2020-10-20\n\n'
    ret += 'Last updated: {}\n'.format(datetime.date.today())
    return ret


def format_summary(data):
    data = sorted(data, key=lambda x: x[2] - x[1])
    ret = '# TA記録（5秒落ち以内）\n\n'
    ret += make_markdown_table(filter(lambda x: x[2] - x[1] <= 5, data))
    return ret


def format_all(data):
    data = sorted(data, key=lambda x: x[2] - x[1])
    ret = '# 全コース記録\n\n'
    ret += make_markdown_table(data)
    return ret


def format_updates(data):
    data = sorted(data, key=lambda x: x[-1])[::-1]
    ret = '# 全コース記録（新しい順）\n\n'
    ret += make_markdown_table(data)
    return ret


with open('README.md', 'w') as f:
    f.write(format_summary(data))
    f.write('\n')
    f.write('[全記録](https://github.com/xuzijian629/xuzijian629/blob/master/ALL.md)')

with open('ALL.md', 'w') as f:
    f.write(format_all(data))

with open('UPDATES.md', 'w') as f:
    f.write(format_updates(data))
