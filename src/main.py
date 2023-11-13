import requests
from bs4 import BeautifulSoup
import re
import time
import os
import random


def get_article_html(url):
    # 获取文章页面内容
    response = requests.get(url)
    return response.text


def get_article(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    # 获取文章标题
    title = soup.find('p', class_='text-title').get_text()
    # 获取文章作者
    author = soup.find('p', class_='text-author').get_text()
    # 获取文章引言
    intro = soup.select('div.one-quote-warp p')[0].get_text()
    # 获取页面所有主要内容
    content = soup.find('div', class_='text-content')
    p_tags = content.findChildren('p', recursive=True)

    # 拼接文章内容

    article = f"""{title}
{author}
“{intro}”\n
"""

    # 添加正文内容
    for p in p_tags[2:]:
        article += p.get_text() + '\n'

    # 添加文章链接
    article += f'\n文章来源：{url}'
    return article


def count_characters(article, include_punctuation):
    # 字数统计
    if include_punctuation:
        return len(article)
    else:
        return len(re.findall(r'\w', article))


# 计时开始
def start_timer():
    return time.time()


# 计时结束
def stop_timer(start_time):
    return time.time() - start_time


def clear_screen():
    if os.name == 'nt':  # 对于Windows系统
        os.system('cls')
    else:  # 对于Mac和Linux系统
        os.system('clear')


def calculate_reading_stats(total_time, total_chars, total_chars_no_punct):
    # 计算各种统计信息
    chars_per_minute = round((total_chars / total_time) * 60, 4)
    chars_per_minute_no_punct = round((total_chars_no_punct / total_time) * 60, 4)
    seconds_per_char = round(total_time / total_chars, 4)
    seconds_per_char_no_punct = round(total_time / total_chars_no_punct, 4)
    return total_time, chars_per_minute, chars_per_minute_no_punct, seconds_per_char, seconds_per_char_no_punct


def main(url):
    html = get_article_html(url)
    article = get_article(html, url)
    total_chars = count_characters(article, True)
    total_chars_no_punct = count_characters(article, False)

    print(f"\n文章获取成功！")
    input("准备完成后按回车键开始计时阅读...")
    clear_screen()
    start_time = start_timer()

    print(article)
    input("阅读完成后按回车键结束...")
    total_time = stop_timer(start_time)
    total_time, chars_per_minute, chars_per_minute_no_punct, seconds_per_char, seconds_per_char_no_punct = \
        calculate_reading_stats(total_time, total_chars, total_chars_no_punct)

    clear_screen()
    print("您的统计信息如下：")
    print(f"总用时: {total_time}秒\n")
    print("（含标点）")
    print(f"总字数: {total_chars}")
    print(f"平均每分钟: {chars_per_minute} 字")
    print(f"平均每字: {seconds_per_char} 秒）\n")
    print("（不含标点）")
    print(f"总字数: {total_chars_no_punct}")
    print(f"平均每分钟: {chars_per_minute_no_punct} 字")
    print(f"平均每字: {seconds_per_char_no_punct} 秒\n")


if __name__ == '__main__':
    article_id_list = [
        6163, 6161, 6160, 6159, 6158,
        6155, 6154, 6156, 6152, 6151,
        6150, 6149, 6144, 6148, 6146,
        6143, 6145, 6138, 6142, 6140,
        6139, 6141, 6131, 6136, 6137,
        6133, 6134, 6132, 6129, 6128,

    ]

    clear_screen()

    print("欢迎使用此阅读能力测试工具")
    print("本工具由星隅(shingyu)开发")
    print("本工具仅供学习交流使用，请勿用于商业用途")
    print("本工具所有文章来自 「ONE  ·  一个」 APP")
    print("著作权归原作者所有")
    print("已收录 " + str(len(article_id_list)) + " 篇文章")
    print("测试时将从中随机选取\n")
    input("按Enter键继续...")

    article_id = str(random.choice(article_id_list))

    url_ = f'http://m.wufazhuce.com/article/{article_id}'
    main(url_)
