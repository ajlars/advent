from datetime import datetime

f = open('adventInputs/dayNine.txt', 'r')

start_time = datetime.now()

file_input = f.read()
mini_input = '2333133121414131402'

def main():
    # calculate(mini_input, True)
    calculate(file_input)
    print(f'Process complete after {datetime.now() - start_time}')

def calculate(input, log = False):
    file_block = get_block(input, True)
    if log: print('parsed file_block', file_block)
    parsed_time = datetime.now()
    print(f'Parsed file_block after {parsed_time - start_time}')
    condensed_block = clean_block(file_block, True)
    condensed_time = datetime.now()
    print(f'Condensed file_block after {condensed_time - parsed_time}')
    if log: print('condensed file_block', condensed_block)
    checksum = get_checksum(condensed_block, True)
    checksum_time = datetime.now()
    print(f'Calculated checksum after {checksum_time - condensed_time}')
    print('checksum', checksum)

def get_block(input, group=False):
    file_block = []
    is_file = True
    id = 0
    for i in input:
        # print(f'i: {i}')
        sub_block = []
        for j in range(int(i)):
            sub_block.append(id if is_file else '.')
        if group and sub_block != []:
            # print(f'sub_block: {sub_block}')
            file_block.append(sub_block)
        else:
            file_block += sub_block
        if is_file:
            id+=1
            is_file = False
        else:
            is_file = True
    return file_block

def clean_block(block, group=False):
    first_empty = 0
    did_change = True
    change = 0
    while(did_change):
        did_change = False
        print(change)
        if(group):
            for i in range(len(block))[::-1]:
                # print(i)
                # if not did_change:
                    # print(f'item: {block[i]}, i: {i}, block length: {len(block)}, index: {len(block) - i -1}')
                if '.' not in block[i]:
                    item = block[i]
                    min_size = len(item)
                    first_empty = False
                    for j, _item in enumerate(block):
                        if '.' in _item and j < i and len(_item) >= min_size:
                            first_empty = j
                            block_a = _item[:min_size]
                            block_b = _item[min_size:]
                            break
                    if(first_empty):
                        # if not did_change:
                            # print(f'first_empty: {first_empty}, block_a: {block_a}, block_b: {block_b}\n{block}')
                        block.insert(first_empty, item)
                        # print(f'post insert of {item} to {first_empty} \n{block}')
                        block[i + 1] = block_a
                        # print(f'used block_a {block_a} to replace original item {i +1}\n{block}')
                        if '.' in block_b:
                            block[first_empty + 1] = block_b
                            # print(f'used block_b {block_b} to replace original empty {first_empty +1}\n{block}')
                        else:
                            block.pop(first_empty + 1)
                            # print(f'removed original empty from {first_empty + 1}\n{block}')
                        did_change = True
                        change += 1
                        break
        else:
            for i, item in enumerate(reversed(block)):
                index = len(block) - i - 1
                if item != '.':
                    try:
                        first_empty = block.index('.', first_empty, index)
                    except ValueError:
                        first_empty = False
                    if(first_empty):
                        block[first_empty] = block[index]
                        block[index] = '.'
    return block

def get_checksum(block, group=False):
    checksum = 0
    if(group):
        _block = [id for ids in block for id in ids]
    else:
        _block = block
    for i, item in enumerate(_block):
        if item != '.':
            checksum += item * i
    return checksum

main()