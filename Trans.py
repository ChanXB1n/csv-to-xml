import csv
import codecs
import re
from xml.etree.ElementTree import ElementTree,Element

reader = csv.reader(open("test.csv"))
headers = next(reader)


def read_xml(in_path):
    '''''读取并解析xml文件
       in_path: xml路径
       return: ElementTree'''
    tree = ElementTree()
    tree.parse(in_path)
    return tree


def write_xml(tree, out_path):
    '''''将xml文件写出
       tree: xml树
       out_path: 写出路径'''
    tree.write(out_path, encoding="utf-8", xml_declaration=True)


def if_match(node, kv_map):
    '''''判断某个节点是否包含所有传入参数属性
       node: 节点
       kv_map: 属性及属性值组成的map'''
    for key in kv_map:
        if node.get(key) != kv_map.get(key):
            return False
    return True


# ---------------search -----

def find_nodes(tree, path):
    '''''查找某个路径匹配的所有节点
       tree: xml树
       path: 节点路径'''
    return tree.findall(path)


def get_node_by_keyvalue(nodelist, kv_map):
    '''''根据属性及属性值定位符合的节点，返回节点
       nodelist: 节点列表
       kv_map: 匹配属性及属性值map'''
    result_nodes = []
    for node in nodelist:
        if if_match(node, kv_map):
            result_nodes.append(node)
    return result_nodes


# ---------------change -----

def change_node_properties(nodelist, kv_map, is_delete=False):
    '''''修改/增加 /删除 节点的属性及属性值
       nodelist: 节点列表
       kv_map:属性及属性值map'''
    for node in nodelist:
        for key in kv_map:
            if is_delete:
                if key in node.attrib:
                    del node.attrib[key]
            else:
                node.set(key, kv_map.get(key))


def change_node_text(nodelist, text, is_add=False, is_delete=False):
    '''''改变/增加/删除一个节点的文本
       nodelist:节点列表
       text : 更新后的文本'''
    for node in nodelist:
        if is_add:
            node.text += text
        elif is_delete:
            node.text = ""
        else:
            node.text = text


def create_node(tag, property_map, content):
    '''''新造一个节点
       tag:节点标签
       property_map:属性及属性值map
       content: 节点闭合标签里的文本内容
       return 新节点'''
    element = Element(tag, property_map)
    element.text = content
    return element


def add_child_node(nodelist, element):
    '''''给一个节点添加子节点
       nodelist: 节点列表
       element: 子节点'''
    for node in nodelist:
        node.append(element)


def del_node_by_tagkeyvalue(nodelist, tag, kv_map):
    '''''同过属性及属性值定位一个节点，并删除之
       nodelist: 父节点列表
       tag:子节点标签
       kv_map: 属性及属性值列表'''
    for parent_node in nodelist:
        children = parent_node.getchildren()
        for child in children:
            if child.tag == tag and if_match(child, kv_map):
                parent_node.remove(child)


def cut_text(text,lenth):
    textArr = re.findall('.{'+str(lenth)+'}', text)
    textArr.append(text[(len(textArr)*lenth):])
    return textArr


def to_unicode(str_to_unicode):
    str_to_unicode = str_to_unicode.encode('unicode_escape').decode('utf-8').upper().replace("\\U", "&#x")
    str_to_unicode_split = str_to_unicode.split("&")

    str_cut = ""
    str_to_unicode = ""

    for index in range(len(str_to_unicode_split)):
        if(len(str_to_unicode_split[index])<=6):
            if (index != 0):
                str_to_unicode += "&" + str_to_unicode_split[index] + ";"
        else:
            str_cut = cut_text(str_to_unicode_split[index],6)
            for j in range(len(str_cut)):
                if (j == 0):
                    str_to_unicode += "&" + str_cut[j] + ";"
                else:
                    str_to_unicode += str_cut[j]
    return str_to_unicode


def add_text(path, text):
    text_nodes = get_node_by_keyvalue(find_nodes(tree, path), {})
    change_node_text(text_nodes, text)


country = to_unicode("中国")
province = to_unicode("广东")
city = to_unicode("汕头")
InCollection = to_unicode("汕头埠老街市图片库")

if __name__ == "__main__":
    # 1. 读取xml文件
    tree = read_xml("template.xml")
    for title, subTitle, namePart, dateIssued, abstract, note, topic, citySection in reader:
        fileName = title + ".xml"
        writer = codecs.open(fileName, "w", "utf-8-sig")
        title = to_unicode(title)
        subTitle = to_unicode(subTitle)
        namePart = to_unicode(namePart)
        dateIssued = dateIssued.replace("/", "-")
        abstract = to_unicode(abstract)
        note = to_unicode(note)
        citySection = to_unicode(citySection)
        add_text("titleInfo/title", title)
        add_text("titleInfo/subTitle", subTitle)
        add_text("name/namePart", namePart)
        add_text("originInfo/dateIssued", dateIssued)
        add_text("abstract", abstract)
        add_text("note", note)
        topicSplit = topic.split(",")
        for index in range(len(topicSplit)):
            topicSplit[index] = to_unicode(topicSplit[index])
            nodes = find_nodes(tree, "subject")
            a = create_node("topic", {}, topicSplit[index])
            add_child_node(nodes, a)
        add_text("subject/hierarchicalGeographic/country", country)
        add_text("subject/hierarchicalGeographic/province", province)
        add_text("subject/hierarchicalGeographic/city", city)
        add_text("subject/hierarchicalGeographic/citySection", citySection)
        add_text("InCollection", InCollection)
        write_xml(tree, fileName)

