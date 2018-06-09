from anytree import Node, RenderTree

ktm_locations = []
outside_locations = []

nepal = Node("nepal", parent=None)

kathmandu = Node("kathmandu", parent=nepal)
sunsari = Node("sunsari", parent=nepal)
kaski = Node("kaski", parent=nepal)
gulmi = Node("gulmi", parent=nepal)
kavre = Node("kavre", parent=nepal)

baneshwor = Node("baneshwor", parent=kathmandu)
koteshwor = Node("koteshwor", parent=kathmandu)
lagankhel = Node("lagankhel", parent=kathmandu)
sinamangal = Node("sinamangal", parent=kathmandu)

class LocationInformation:

    def all_ktm_locations(self):
        for row in RenderTree(kathmandu):
            if row.node.parent == kathmandu:
                ktm_locations.append(row.node.name)
        return ktm_locations

    def all_locations(self):
        for row in RenderTree(nepal):
            if row.node.parent == nepal:
                outside_locations.append(row.node.name)
        return outside_locations

# a = LocationInformation()
# print (a.all_locations())