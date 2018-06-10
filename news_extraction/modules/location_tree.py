from anytree import Node, RenderTree

ktm_locations = []
outside_locations = []

nepal = Node("nepal", parent=None)

jhapa = Node("", parent=nepal)
ilam = Node("ilam", parent=nepal)
panchthar = Node("panchthar", parent=nepal)
taplejung = Node("taplejung", parent=nepal)
morang = Node("morang", parent=nepal)
sunsari = Node("sunsari", parent=nepal)
bhojpur = Node("bhojpur", parent=nepal)
dhankuta = Node("dhankuta", parent=nepal)
terhathum = Node("terhathum", parent=nepal)
sankhuwasabha = Node("sankhuwasabha", parent=nepal)
saptari = Node("saptari", parent=nepal)
siraha = Node("siraha", parent=nepal)
udayapur = Node("udayapur", parent=nepal)
khotang = Node("khotang", parent=nepal)
okhaldhunga = Node("okhaldhunga", parent=nepal)
solukhumbu = Node("solukhumbu", parent=nepal)
dhanusa = Node("dhanusa", parent=nepal)
mahottari = Node("mahottari", parent=nepal)
sarlahi = Node("sarlahi", parent=nepal)
sindhuli = Node("sindhuli", parent=nepal)
ramechhap = Node("ramechhap", parent=nepal)
dolakha = Node("dolakha", parent=nepal)
bhaktapur = Node("bhaktapur", parent=nepal)
dhading = Node("dhading", parent=nepal)
kathmandu = Node("kathmandu", parent=nepal)
kavrepalanchok = Node("kavrepalanchok", parent=nepal)
lalitpur = Node("lalitpur", parent=nepal)
nuwakot = Node("nuwakot", parent=nepal)
rasuwa = Node("rasuwa", parent=nepal)
sindhupalchok = Node("sindhupalchok", parent=nepal)
bara = Node("bara", parent=nepal)
parsa = Node("parsa", parent=nepal)
rautahat = Node("rautahat", parent=nepal)
chitwan = Node("chitwan", parent=nepal)
makwanpur = Node("makwanpur", parent=nepal)
gorkha = Node("gorkha", parent=nepal)
kaski = Node("kaski", parent=nepal)
lamjung = Node("lamjung", parent=nepal)
syangja = Node("syangja", parent=nepal)
tanahun = Node("tanahun", parent=nepal)
manang = Node("manang", parent=nepal)
kapilvastu = Node("kapilvastu", parent=nepal)
nawalparasi = Node("nawalparasi", parent=nepal)
rupandehi = Node("rupandehi", parent=nepal)
arghakhanchi = Node("arghakhanchi", parent=nepal)
gulmi = Node("gulmi", parent=nepal)
palpa = Node("palpa", parent=nepal)
baglung = Node("baglung", parent=nepal)
myagdi = Node("myagdi", parent=nepal)
parbat = Node("parbat", parent=nepal)
mustang = Node("mustang", parent=nepal)
dang = Node("dang", parent=nepal)
pyuthan = Node("pyuthan", parent=nepal)
rolpa = Node("rolpa", parent=nepal)
rukum = Node("rukum", parent=nepal)
salyan = Node("salyan", parent=nepal)
dolpa = Node("dolpa", parent=nepal)
humla = Node("humla", parent=nepal)
jumla = Node("jumla", parent=nepal)
kalikot = Node("kalikot", parent=nepal)
mugu = Node("mugu", parent=nepal)
banke = Node("banke", parent=nepal)
bardiya = Node("bardiya", parent=nepal)
surkhet = Node("surkhet", parent=nepal)
dailekh = Node("dailekh", parent=nepal)
jajarkot = Node("jajarkot", parent=nepal)
kailali = Node("kailali", parent=nepal)
achham = Node("achham", parent=nepal)
doti = Node("doti", parent=nepal)
bajhang = Node("bajhang", parent=nepal)
bajura = Node("bajura", parent=nepal)
kanchanpur = Node("kanchanpur", parent=nepal)
dadeldhura = Node("dadeldhura", parent=nepal)
baitadi = Node("baitadi", parent=nepal)
darchula = Node("darchula", parent=nepal)

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