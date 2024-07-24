import os
import subprocess
from gxl_ai_utils.utils import utils_file

input_json_dir = "/home/work_nfs13/xlgeng/data/MSR-86K/MSR-86K"

language_name, _ = utils_file.do_listdir(input_json_dir, return_path=False)

utils_file.logging_print('先统计所有的音频条目数')
total_num = 0
err_dict_path = './err.json'
if os.path.exists(err_dict_path):
    err_dict = utils_file.load_dict_from_json(err_dict_path)
else:
    err_dict = {}


def func_little4language(language,input_audio_dict_list, output_dir):
    """"""
    utils_file.makedir(output_dir)
    total_wav_num = len(input_audio_dict_list)
    for i, input_audio_dict in enumerate(input_audio_dict_list):
        try:
            utils_file.logging_print(f'{language} wav schedule {i}/{total_wav_num}')
            wav_name = input_audio_dict['aid']
            source_wav_path = os.path.join(output_dir, wav_name + '.mp3')
            if os.path.exists(source_wav_path):
                utils_file.logging_print(f'{language} wav {i}/{total_wav_num} 已经存在, 跳过')
                continue
            utils_file.do_download_from_play_url(input_audio_dict['url'], output_dir, wav_name=wav_name, wav_type='mp3')
            if not os.path.exists(source_wav_path):
                err_dict[input_audio_dict['aid']] = {'url': input_audio_dict['url'], 'output_dir': output_dir}
        except Exception as e:
            utils_file.logging_print(f'{e}')
            err_dict[input_audio_dict['aid']] = {'url': input_audio_dict['url'], 'output_dir': output_dir}


def func_little4split_wav(input_audio_dict, input_wav_path, res_wav_dict, res_text_dict):
    """"""
    now_time = utils_file.do_get_now_time()
    utils_file.logging_print('开始处理：', input_wav_path)
    normalization_wav_path = input_wav_path.replace('.wav', '_normalization.wav')
    utils_file.logging_print('开始标准化')
    utils_file.do_normalization(input_wav_path, normalization_wav_path)
    utils_file.logging_print('开始分割')
    segment_list = input_audio_dict['segments']
    total_seg = len(segment_list)
    for i, segment_info_dict in enumerate(segment_list):
        utils_file.logging_print(f'input_wav: {input_wav_path}, segment schedule: {i + 1}/{total_seg}')
        sid = segment_info_dict["sid"]
        sid_name = sid + ".wav"
        begin_time = segment_info_dict["begin_time"]
        end_time = segment_info_dict["end_time"]
        text = segment_info_dict["text_tn"]
        seg_wav_path = utils_file.do_replace_name(normalization_wav_path, sid_name)
        utils_file.do_extract_audio_segment(normalization_wav_path, seg_wav_path, int(begin_time * 16000),
                                            int(end_time * 16000))
        res_wav_dict[sid] = seg_wav_path
        res_text_dict[sid] = text
    utils_file.logging_print(f'删除{normalization_wav_path} and {input_wav_path}')
    utils_file.remove_file(normalization_wav_path)
    utils_file.remove_file(input_wav_path)
    utils_file.logging_print(f'处理完成，耗时{utils_file.do_get_elapsed_time(now_time)}s input_wav:', input_wav_path)

runner = utils_file.GxlDynamicThreadPool()
root_dir = "/home/work_nfs13/xlgeng/data/MSR-86K/MSR-86K/row_wav"
utils_file.makedir(root_dir)
for language in language_name:
    input_json_dir_language = os.path.join(input_json_dir, language)
    dev_json_path = os.path.join(input_json_dir_language, 'dev.json')
    train_json_path = os.path.join(input_json_dir_language, 'train.json')
    if not os.path.exists(dev_json_path) or not os.path.exists(train_json_path):
        utils_file.logging_print(f'{language} 不存在dev.json或train.json')
        continue
    dev_json_dict = utils_file.load_dict_from_json(dev_json_path)
    train_json_dict = utils_file.load_dict_from_json(train_json_path)
    wav_dict_list = dev_json_dict['audios'] + train_json_dict['audios']
    print(language, len(wav_dict_list))
    output_dir_language = os.path.join(root_dir, language)
    utils_file.makedir(output_dir_language)
    runner.add_thread(func_little4language, [language, wav_dict_list, output_dir_language])

runner.start()
utils_file.logging_print("完全下载完毕")
utils_file.write_dict_to_json(err_dict, err_dict_path)