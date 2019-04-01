# -*- coding: utf-8 -*-
"""该文件包含PyAIML包中其他模块使用的各种通用实用函数。    """
import re
from .LangSupport import splitChinese

def sentences(s):
    """将一堆字符串切分成一个句子列表。"""
    try: s+""
    except: raise TypeError( "s must be a string" )
    pos = 0
    sentenceList = []
    l = len(s)
    while pos < l:
        try: p = s.index('.', pos)
        except: p = l+1
        try: q = s.index('?', pos)
        except: q = l+1
        try: e = s.index('!', pos)
        except: e = l+1
        end = min(p,q,e)
        sentenceList.append( s[pos:end].strip() )
        pos = end+1
    # 如果没有找到句子，则返回一个包含整个输入字符串的单条目列表。
    if len(sentenceList) == 0:
        sentenceList.append(s)
        # 自动转换中文！
    return map(lambda s: u' '.join(splitChinese(s)), sentenceList)

_LIST_PATTERN = re.compile(r"(.*)\[(.*)\](.*)")

def re_split(text):
    """
    >>> a = u"ab sd fc[d | e | f],sd jf,[b | f]"
    >>>     for ia in re_split(text=a):
    >>>         print(ia)
    >>> ab
    >>> sd
    >>> fc
    >>> (u'd', u'e', u'f')
    >>> ,sd
    >>> jf,
    >>> (u'b', u'f')

    :param text:
    :return:
    """
    find_list = _LIST_PATTERN.findall(text)
    if len(find_list) == 0:
        return text.split()
    find_list = find_list[0]
    split_res = re_split(find_list[0])
    split_res += [tuple([i.strip() for i in find_list[1].split(u"|")])]
    split_res += find_list[2].split()
    return split_res