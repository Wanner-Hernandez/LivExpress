def evalify(string):
    html = []
    if string is not None:
        listify = eval(string)

        for hashtag in listify:
            html.append(hashtag)
        return html
    else:
        return ["No Tags"]
    

print(evalify(None))