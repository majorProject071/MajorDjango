from anytree import Node, RenderTree

nepal = Node("nepal", parent=None)
kathmandu = Node("kathmandu"or"ktm" , parent=nepal)
# ktm = Node("ktm", parent=nepal)
ktm = kathmandu

print (kathmandu.path)
print (ktm.path)
print(RenderTree(nepal))