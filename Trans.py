import csv
import codecs
import re
reader = csv.reader(open("test.csv"))
headers = next(reader)


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


country = to_unicode("中国")
province = to_unicode("广东")
city = to_unicode("汕头")
InCollection = to_unicode("汕头埠老街市图片库")


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
    writer.write("<?xml version=\"1.0\"?>\n"
                  + "<mods xmlns=\"http://www.loc.gov/mods/v3\" xmlns:mods=\"http://www.loc.gov/mods/v3\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xlink=\"http://www.w3.org/1999/xlink\">\n"
                  + "\t<titleInfo>\n"
                  + "\t\t<title>"+title+"</title>\n"
                  + "\t\t<subTitle>"+subTitle+"</subTitle>\n"
                  + "\t</titleInfo>\n"

                  + "\t<name type=\"personal\">\n"
                  + "\t\t<namePart>" + namePart + "</namePart>\n"
                  + "\t\t<role>\n"
                  + "\t\t\t<roleTerm authority=\"marcrelator\" type=\"text\"></roleTerm>\n"
                  + "\t\t</role>\n"
                  + "\t</name>\n"

                  + "\t<typeOfResource>still image</typeOfResource>\n"

                  + "\t<genre authority=\"lctgm\"></genre>\n"

                  + "\t<originInfo>\n"
                  + "\t\t<dateIssued>" + dateIssued + "</dateIssued>\n"
                  + "\t\t<publisher></publisher>\n"
                  + "\t\t<place>\n"
                  + "\t\t\t<placeTerm authority=\"marccountry\" type=\"code\"></placeTerm>\n"
                  + "\t\t</place>\n"
                  + "\t\t<place>\n"
                  + "\t\t\t<placeTerm type=\"text\"></placeTerm>\n"
                  + "\t\t</place>\n"
                  + "\t</originInfo>\n"

                  + "\t<language>\n"
                  + "\t\t<languageTerm authority=\"iso639-2b\" type=\"code\"></languageTerm>\n"
                  + "\t</language>\n"

                  + "\t<abstract>" + abstract + "</abstract>\n"

                  + "\t<identifier type=\"local\"></identifier>\n"

                  + "\t<physicalDescription>\n"
                  + "\t\t<form authority=\"marcform\">nonprojected graphic</form>\n"
                  + "\t\t<extent></extent>\n"
                  + "\t</physicalDescription>\n"

                  + "\t<note>" + note + "</note>\n"

                  + "\t<subject>\n"
                  + "\t\t<topic></topic>\n")
    topicSplit = topic.split(",")
    for index in range(len(topicSplit)):
        topicSplit[index] = to_unicode(topicSplit[index])
        writer.write("\t\t<topic>" + topicSplit[index] + "</topic>\n")

    writer.write("\t\t<geographic></geographic>\n"
                 + "\t\t<temporal></temporal>\n"
                 + "\t\t<hierarchicalGeographic>\n"
                 + "\t\t\t<continent></continent>\n"
                 + "\t\t\t<country>" + country+ "</country>\n"
                 + "\t\t\t<province>" + province + "</province>\n"
                 + "\t\t\t<region></region>\n"
                 + "\t\t\t<county></county>\n"
                 + "\t\t\t<city>" + city + "</city>\n"
                 + "\t\t\t<citySection>" + citySection + "</citySection>\n"
                 + "\t\t</hierarchicalGeographic>\n"
                 + "\t\t<cartographics>\n"
                 + "\t\t\t<coordinates></coordinates>\n"
                 + "\t\t</cartographics>\n"
                 + "\t</subject>\n"

                 + "\t<InCollection>" + InCollection + "</InCollection>\n"

                 + "</mods>")
    writer.close()


