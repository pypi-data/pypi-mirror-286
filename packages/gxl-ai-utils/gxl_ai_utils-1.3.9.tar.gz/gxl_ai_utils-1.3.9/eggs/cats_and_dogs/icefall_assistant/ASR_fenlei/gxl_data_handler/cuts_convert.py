from gxl_ai_utils.utils import utils_file

input_cuts_path = "/home/work_nfs8/xlgeng/new_workspace/icefall/egs/aishell/ASR/gxl_data/fbank_common/gxldata_cuts_test.jsonl"
onput_cuts_path = "/home/work_nfs8/xlgeng/new_workspace/icefall/egs/aishell/ASR/gxl_data/fbank_common/gxldata_cuts_test_2.jsonl"

fake_words = {
    "国家": ["中国", "美国", "英国", "法国", "德国", "日本", "韩国", "澳大利亚", "新西兰", "加拿大", "巴西", "印度",
             "阿根廷", "南非", "俄罗斯", "巴基斯坦", "伊朗", "阿富汗", "埃及", "尼日利亚", "乌干达", "肯尼亚", "马拉维",
             "坦桑尼亚", "赞比亚", "莫桑比克", "津巴布韦", "毛里求斯", "塞拉利昂", "毛里塔尼亚", "马里", "塞内加尔",
             "尼日尔", "多哥", "贝宁", "布基纳法索", "科特迪瓦", "加纳", "尼日利亚", "喀麦隆", "乍得", "刚果",
             "刚果民主共和国", "赤道几内亚", "加蓬", "冈比亚", "几内亚比绍", "利比里亚", "马达加斯加", "马尔加斯尔",
             "马里亚纳群岛", "马里亚纳群岛", "马约特岛", "毛里塔尼亚", "尼日利亚", "塞舌尔", "塞拉利昂", "塞内加尔",
             "索马里", "索马里兰和科摩罗", "坦桑尼"],
    "日期": ["星期", "年", "月", "日", "号", "日"],
    "自然灾害": ['火灾', '地震', '洪水', '泥石流', '台风', '冰雹', '雪灾', '旱灾', '风灾', '雷电', '霜冻', '冰冻',
                 '暴雨', '冰雹'],
    "天气": ["晴", "阴", "雨", "雪", "雾", "风", "雷", "霜", "冰", "雹", "霜冻", "冰冻", "暴雨", "冰雹"],
    "气候": ["温和", "寒冷", "炎热", "湿润", "干燥", "潮湿", "干旱", "风", "雨", "雾", "雪", "冰雹", "霜冻", "冰冻",
             "暴雨"],
    "地名省会": ["厦门", "福州", "郑州", "北京", "天津", "上海", "广州", "深圳", "杭州", "成都", "重庆", "武汉", "长沙",
                 "南京", "苏州", "无锡", "济南", "青岛", "沈阳", "大连", "长春", "哈尔滨", "石家庄", "太原", "西安",
                 "银川", "兰州", "西宁", "乌鲁木齐"]
}

dict_list = utils_file.load_dict_list_from_jsonl(input_cuts_path)


def tag_string(string, fake_words):
    for key, words in fake_words.items():
        for word in words:
            if word in string:
                return key
    return "other"


output_list = []
for dict_item in utils_file.tqdm(dict_list, desc="tagging", total=len(dict_list)):
    dict_item.pop('label')
    dict_item['supervisions'][0]["speaker"] = tag_string(dict_item['supervisions'][0]["text"], fake_words)
    output_list.append(dict_item)

utils_file.write_dict_list_to_jsonl(output_list, onput_cuts_path)
utils_file.do_compress_file_by_gzip(onput_cuts_path)