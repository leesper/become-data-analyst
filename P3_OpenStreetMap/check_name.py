# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

osm_file = 'guiyang_china.osm'

# regular expression for English name
enre = re.compile('[A-Za-z]+.[A-Za-z]+')
# regular expression for Chinese name
chre = re.compile(u'[\u4e00-\u9fa5]+.[\u4e00-\u9fa5]+')

for event, element in ET.iterparse(osm_file, events=("start",)):
    if element.tag in ['node', 'way']:
        name = ''
        name_en = ''
        name_zh = ''
        for tag in element.iter('tag'):
            if tag.attrib['k'] == 'name':
                name = tag.attrib['v'].decode('utf-8')
            elif tag.attrib['k'] == 'name:en':
                name_en = tag.attrib['v'].decode('utf-8')
            elif tag.attrib['k'] == 'name:zh':
                name_zh = tag.attrib['v'].decode('utf-8')

        if name != '' and name_en != '' and name_zh != '':
            # retrieve English name from name
            re_en = ''
            m_en = enre.search(name)
            if m_en:
                re_en = m_en.group()

            if re_en != '' and name_en not in re_en and re_en not in name_en:
                print('id: {} name: {} name_en: {} not match'.format(element.attrib['id'], re_en, name_en))

            #retrieve Chinese name from name
            re_zh = ''
            m_zh = chre.search(name)
            if m_zh:
                re_zh = m_zh.group()

            if re_zh != '' and name_zh not in re_zh and re_zh not in name_zh:
                print('id: {} name: {} name_zh: {} not match'.format(element.attrib['id'], re_zh, name_zh))
