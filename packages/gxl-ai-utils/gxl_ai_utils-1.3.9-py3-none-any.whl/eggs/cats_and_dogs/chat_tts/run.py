import os
import sys
from gxl_ai_utils.utils import utils_file

if sys.platform == "darwin":
    os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

now_dir = os.getcwd()
sys.path.append("/home/work_nfs8/xlgeng/new_workspace/ChatTTS")

import argparse

import ChatTTS

from tools.audio import wav_arr_to_mp3_view
from tools.logger import get_logger

logger = get_logger("Command")


def save_mp3_file(wav, index, output_dir="./"):
    data = wav_arr_to_mp3_view(wav)
    mp3_filename = f"{index}.mp3"
    output_path = os.path.join(output_dir, mp3_filename)
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(data)
    logger.info(f"Audio saved to {mp3_filename}")


def main(texts: list[str], keys: list[str]):
    logger.info("Text input: %s", str(texts))

    chat = ChatTTS.Chat(get_logger("ChatTTS"))
    logger.info("Initializing ChatTTS...")
    if chat.load():
        logger.info("Models loaded successfully.")
    else:
        logger.error("Models load failed.")
        sys.exit(1)
    for index, text in utils_file.tqdm(texts, total=len(texts)):
        utils_file.logging_print('processing: ' + text)
        wavs_i = chat.infer([text], use_decoder=True)
        utils_file.logging_print('得到' + str(len(wavs_i)) + '个wav')
        wav_i = wavs_i[0]
        utils_file.logging_print('开始保存')
        save_mp3_file(wav_i, keys[index], "/home/work_nfs14/xlgeng/wav_tts")
    utils_file.logging_print(f'finish all .............')


if __name__ == "__main__":
    input_jsonl_path = "/home/work_nfs8/xlgeng/new_workspace/gxl_ai_utils/eggs/cats_and_dogs/chat_tts/xiaohuangji50w_nofenci.josnl"
    dict_list = utils_file.load_dict_list_from_jsonl(input_jsonl_path)
    texts = [x["Q"] for x in dict_list]
    keys = [x["key"] for x in dict_list]
    main(texts, keys)
    logger.info("TTS application finished.")
