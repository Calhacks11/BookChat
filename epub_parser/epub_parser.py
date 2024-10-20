from epub2txt import epub2txt
# from a url to epub
# url = "https://github.com/ffreemt/tmx2epub/raw/master/tests/1.tmx.epub"
# res = epub2txt(url, outputlist=True)

# # from a local epub file
filepath = 'shaw-caesar-and-cleopatra.epub'
res = epub2txt(filepath)

# output as a list of chapters
# ch_list = epub2txt(filepath, outputlist=True)
# chapter titles will be available as epub2txt.content_titles if available
print(res)