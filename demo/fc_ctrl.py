import pyautogui
import time
import sys
sys.path.append('.')
from utils.anno.cls.text_classification import text_classification

input_trans = {
    '跳': 'g',
    '向右走': 'd',
    '向左走': 'a',
}

def do(results):
    time.sleep(0.05)
    pyautogui.getWindowsWithTitle('nes')[0].activate()
    # pyautogui.getWindowsWithTitle('1.txt')[0].activate()

    # time.sleep(1)

    for result in results:
        key = input_trans[result]
        pyautogui.keyDown(key)
    time.sleep(0.3)
    for result in results:
        key = input_trans[result]
        pyautogui.keyUp(key)
    time.sleep(0.05)

    pyautogui.getWindowsWithTitle('fc_ctrl')[0].activate()

if __name__ == '__main__':
    while True:
        text = input('用户输入: ')
        results = text_classification(text, ['跳', '向右走', '向左走'])
        print(results)
        # do(['跳'])
        # do([text])
        do(results)
