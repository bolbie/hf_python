phrase = "Don't panic!"
plist = list(phrase)
print(phrase)
print(plist)

for i in range(4):
    plist.pop()
plist.pop(0)
plist.remove("'")
plist.insert(-1, plist.pop(2))
plist.append(plist.pop(3))

new_phrase = ''.join(plist)
print(plist)
print(new_phrase)
