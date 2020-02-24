import os


def parseUrlsFromFile(filepath):
    urls = []
    if os.path.isfile(filepath):
        print("--- Reading Input File ---")
        with open(filepath) as fp:
            cnt = 0
            for line in fp:
                if(len(line) > 1):
                    link = ""
                    if("//" in line):
                        parts = line.split("//", 1)
                        link = parts[1] if len(parts) > 1 else parts[0]
                        link = link.split(' ')[0].rstrip().replace(
                            "[", '').replace(']', '')
                    else:
                        if(" " in line):
                            link = line.split(' ')[1].rstrip().replace(
                                "[", '').replace(']', '')
                    if(len(link) <= 1):
                        link = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line)
                    else:
                        if(len(link) > 1 and link not in urls):
                            urls.append(link)
                            print("Link {}:  -   {}".format(cnt, link))

                    if(cnt % 10 == 0):
                        pass
                        # print()
                    cnt += 1
    return urls
