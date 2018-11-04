#[{},{}][{}]
def judge_file_already_transmit(current_file_info, transmit_file_info_lists):
    '''
        describe：
                            如果有文件新增、文件内容被改变。都需要重新传输。
        para：
            current_file_info_lists：实时遍历当前文件 列表，是否存在新增文件，文件内容是否已经改变。
            transmit_file_info_lists： 已经传输完成的文件 列表。
        return:
            False: 文件没有传输
            True: 文件已经传输
    '''
    for transmit_file_info in transmit_file_info_lists:
        if transmit_file_info['filename'] == current_file_info['filename']:
            if transmit_file_info['md5sum'] == current_file_info['md5sum']:
                return True
    return False
            