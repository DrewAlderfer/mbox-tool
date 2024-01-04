import re
from glob import iglob
import mailbox

def measure_string(text):
    return int(len(text.encode('utf-8')) / 1000)

def save_file(blocks, base_name='emails', output_dir='.'):
    for i, (emails, _, _) in enumerate(blocks):
        filename = f"{base_name}_{i:03d}.mbox" 
        with open(f"{output_dir}/{filename}", "w") as file:
            file.writelines(emails)

def mean_error(blocks, target):
    result = 0
    for block in blocks:
        result += target - block[1]
    return result / len(blocks)

def merge_blocks(x, y, target):
    x, xs, _ = x
    y, ys, _ = y
    x.extend(y)

    return x, xs+ys, target - (xs+ys)

def rank_dist(blocks, target):
    dist = []
    for idx, (_, a, _) in enumerate(blocks):
        for jdx, (_, b, _) in enumerate(blocks):
            if idx == jdx:
                continue
            total = a + b
            if total < target:
                dist.append(((idx, jdx), target - (a + b)))
                continue
    dist = sorted(dist, key=lambda x: x[1])
    # print(f"ranked dist:\n{dist}")
    x, y = dist[0][0]
    combination = merge_blocks(blocks[x], blocks[y], target)
    blocks.pop(x)
    blocks.pop(y - 1)
    blocks.append(combination)

    return blocks, dist

def combine_blocks(blocks, target=30000):
    start = len(blocks)
    loops = 0
    while len(blocks) > 1:
        blocks, dist = rank_dist(blocks, target) 
        loops += 1
        if len(dist) == 2:
            break
    end = len(blocks)
    print(f"combined {start} blocks into {end} blocks after {loops} iterations")
    return blocks

def email_blocks(block_size:int=1000, filter:int=30000):
    with open("./emails.mbox", "r") as file:
        string = file.read()
    mbox = re.split(r'^From\s', string, flags=re.MULTILINE)
    mbox = mbox[1:]
    file_size = 0
    emails = []
    blocks = []
    sec = []
    div = 1
    for num, email in enumerate(mbox):
        if measure_string(email) > filter:
            print(f"email {num} is {measure_string(email)} KiB")
            mbox.remove(email)
    print(f"found {len(mbox)} emails")

    for cursor, message in enumerate(mbox):
        if file_size + measure_string(message) > block_size:
            blocks.append((emails, file_size, block_size - file_size))
            emails = []
            sec = []
            file_size = measure_string(message)
            emails.append(f"From {message}")
            div += 1
            continue

        emails.append(f"From {message}")
        file_size += measure_string(message)
        sec.append(cursor)

    print("done")
    return blocks

def test_mbox(blocks, dir='/mnt/c/Users/drew/emails'):
    files = iglob(f"{dir}/*.mbox")
    for file, (block, _, _) in zip(files, blocks):
        mbox = mailbox.mbox(file)
        print(len(mbox), len(block))
    print("done")
