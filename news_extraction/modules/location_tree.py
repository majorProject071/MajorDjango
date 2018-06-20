from anytree import Node, RenderTree

ktm_locations = []
ltp_locations = []
bkt_locations = []
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
kavre = Node("kavre", parent=nepal)
lalitpur = Node("lalitpur", parent=nepal)
nuwakot = Node("nuwakot", parent=nepal)
rasuwa = Node("rasuwa", parent=nepal)
sindhupalchok = Node("sindhupalchok", parent=nepal)
bara = Node("bara", parent=nepal)
parsa = Node("parsa", parent=nepal)
rautahat = Node("rautahat", parent=nepal)
chitwan = Node("chitawan", parent=nepal)
chitawan = Node("chitawan", parent=nepal)
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

chabahil = Node("chabahil", parent=kathmandu)
sukedhara = Node("sukedhara", parent=kathmandu)
dhumbarahi = Node("dhumbarahi", parent=kathmandu)
maharajgunj = Node("maharajgunj", parent=kathmandu)
balaju = Node("balaju", parent=kathmandu)
basundhara = Node("basundhara", parent=kathmandu)
samakhusi = Node("samakhusi", parent=kathmandu)
gongabu = Node("gongabu", parent=kathmandu)
narayan_gopal_chowk = Node("narayan gopal chowk", parent=kathmandu)
new_buspark = Node("new buspark", parent=kathmandu)
machhapokhari = Node("machha pokhari", parent=kathmandu)
dhungedhara = Node("dhungedhara", parent=kathmandu)
sano_bharyang = Node("sano bharyang", parent=kathmandu)
thulo_bharyang = Node("thulo bharyang", parent=kathmandu)
banasthali = Node("banasthali", parent=kathmandu)
swoyambhu = Node("swoyambhu", parent=kathmandu)
chhauni = Node("chhauni", parent=kathmandu)
halchok = Node("halchok", parent=kathmandu)
sitapaila = Node("sitapaila", parent=kathmandu)
tahachal = Node("tahachal", parent=kathmandu)
syuchatar = Node("syuchatar", parent=kathmandu)
old_naikap = Node("old naikap", parent=kathmandu)
new_naikap = Node("new naikap", parent=kathmandu)
kalimati = Node("kalimati", parent=kathmandu)
kalanki = Node("kalanki", parent=kathmandu)
ravibhavan = Node("ravibhavan", parent=kathmandu)
kuleshwor = Node("kuleshwor", parent=kathmandu)
sanepa = Node("sanepa", parent=kathmandu)
balkhu = Node("balkhu", parent=kathmandu)
tinthana = Node("tinthana", parent=kathmandu)
dhobighat = Node("dhobighat", parent=kathmandu)
ekantakuna = Node("ekantakuna", parent=kathmandu)
baghdol = Node("baghdol", parent=kathmandu)
chobhar = Node("chobhar", parent=kathmandu)
nakhkhu = Node("nakhkhu", parent=kathmandu)
nayabasti = Node("nayabasti", parent=kathmandu)
kusunti = Node("kusunti", parent=lalitpur)
satdobato = Node("satdobato", parent=lalitpur)
khumaltar = Node("khumaltar", parent=lalitpur)
gwarko = Node("gwarko", parent=lalitpur)
koteshwor = Node("koteshwor", parent=kathmandu)
subidhanagar = Node("subidhanagar", parent=kathmandu)
tinkune = Node("tinkune", parent=kathmandu)
gairigaon = Node("gairigaon", parent=kathmandu)
jagritinagar = Node("jagritinagar", parent=kathmandu)
sinamangaal = Node("sinamangaal", parent=kathmandu)
gaucharan = Node("gaucharan", parent=kathmandu)
airport = Node("airport", parent=kathmandu)
gaushala = Node("gaushala", parent=kathmandu)
battisputali = Node("battisputali", parent=kathmandu)
siphal = Node("siphal", parent=kathmandu)
boudha = Node("boudha", parent=kathmandu)
jorpati = Node("jorpati", parent=kathmandu)
makalbari = Node("makalbari", parent=kathmandu)
mulpani = Node("mulpani", parent=kathmandu)
danchhi = Node("danchhi", parent=kathmandu)
bhadrabas = Node("bhadrabas", parent=kathmandu)
sankhu = Node("sankhu", parent=kathmandu)
gaurighat = Node("gaurighat", parent=kathmandu)
kumarigal = Node("kumarigal", parent=kathmandu)
old_baneshwor = Node("old baneshwor", parent=kathmandu)
new_baneshwor = Node("new baneshwor", parent=kathmandu)
baneshwor = Node("baneshwor", parent=kathmandu)
bhimsengola = Node("bhimsengola", parent=kathmandu)
mahadevsthan = Node("mahadevsthan", parent=kathmandu)
anamnagar = Node("anamnagar", parent=kathmandu)
thapagaon = Node("thapagaon", parent=kathmandu)
minbhavan = Node("minbhavan", parent=kathmandu)
shankhamul = Node("shankhamul", parent=kathmandu)
bhuddhanagar = Node("bhuddhanagar", parent=kathmandu)
shantinagar = Node("shantinagar", parent=kathmandu)
hanumansthan = Node("hanumansthan", parent=kathmandu)
singhadurbar = Node("singhadurbar", parent=kathmandu)
thapathali = Node("thapathali", parent=kathmandu)
jwagal = Node("jwagal", parent=lalitpur)
kupandole = Node("kupandole", parent=lalitpur)
bakhundole = Node("bakhundole", parent=lalitpur)
pulchowk = Node("pulchowk", parent=lalitpur)
chakupat = Node("chakupat", parent=lalitpur)
imukhel = Node("imukhel", parent=lalitpur)
baliphal = Node("baliphal", parent=lalitpur)
patandhoka = Node("patandhoka", parent=lalitpur)
mangalbazaar = Node("mangalbazaar", parent=lalitpur)
kumaripati = Node("kumaripati", parent=lalitpur)
manbhavan = Node("manbhavan", parent=lalitpur)
lagankhel = Node("lagankhel", parent=lalitpur)
thasikhel = Node("thasikhel", parent=lalitpur)
imadol = Node("imadol", parent=lalitpur)
hattiban = Node("hattiban", parent=lalitpur)
shorakhutte = Node("shorakhutte", parent=kathmandu)
kirtipur = Node("kirtipur", parent=kathmandu)
panga = Node("panga", parent=kathmandu)
chandragiri = Node("chandragiri", parent=kathmandu)
gurjudhara = Node("gurjudhara", parent=kathmandu)
satungal = Node("satungal", parent=kathmandu)
tinthana = Node("tinthana", parent=kathmandu)
thankot = Node("thankot", parent=kathmandu)
nagarjun = Node("nagarjun", parent=kathmandu)
ranibari = Node("ranibari", parent=kathmandu)
panipokhari = Node("panipokhari", parent=kathmandu)
goldhunga = Node("goldhunga", parent=kathmandu)
dharmasthali = Node("dharmasthali", parent=kathmandu)
manamaiju = Node("manamaiju", parent=kathmandu)
mudkhu = Node("mudkhu", parent=kathmandu)
bansbari = Node("bansbari", parent=kathmandu)
golfutar = Node("golfutar", parent=kathmandu)
mahankal = Node("mahankal", parent=kathmandu)
tokha = Node("tokha", parent=kathmandu)
budhanilkantha = Node("budhanilkantha", parent=kathmandu)
suntakhan = Node("suntakhan", parent=kathmandu)
baluwa = Node("baluwa", parent=kathmandu)
bhangal = Node("bhangal", parent=kathmandu)
chunikhel = Node("chunikhel", parent=kathmandu)
nayapati = Node("nayapati", parent=kathmandu)
kapan = Node("kapan", parent=kathmandu)
sundarijal = Node("sundarijal", parent=kathmandu)
gokarna = Node("gokarna", parent=kathmandu)
chandol = Node("chandol", parent=kathmandu)
baluwatar = Node("baluwatar", parent=kathmandu)
bhatbhateni = Node("bhatbhateni", parent=kathmandu)
naxal = Node("naxal", parent=kathmandu)
lazimpat = Node("lazimpat", parent=kathmandu)
lainchaur = Node("lainchaur", parent=kathmandu)
thamel = Node("thamel", parent=kathmandu)
narayanhiti = Node("narayanhiti", parent=kathmandu)
bulbule = Node("bulbule", parent=kathmandu)
sano_gaucharan = Node("sano gaucharan", parent=kathmandu)
gyaneshwor = Node("gyaneshwor", parent=kathmandu)
hattisar = Node("hattisar", parent=kathmandu)
durbarmarg = Node("durbarmarg", parent=kathmandu)
kutubahal = Node("kutubahal", parent=kathmandu)
maligaon = Node("maligaon", parent=kathmandu)
kamaladi = Node("kamaladi", parent=kathmandu)
bagbazar = Node("bagbazar", parent=kathmandu)
ghattekulo = Node("ghattekulo", parent=kathmandu)
putalisadak = Node("putalisadak", parent=kathmandu)
bhrikuti_mandap = Node("bhrikuti mandap", parent=kathmandu)
tripureshwor = Node("tripureshwor", parent=kathmandu)
bhotebahal = Node("bhotebahal", parent=kathmandu)
teku = Node("teku", parent=kathmandu)
ason = Node("ason", parent=kathmandu)
indrachowk = Node("indrachowk", parent=kathmandu)
nardevi = Node("nardevi", parent=kathmandu)
chhetrapati = Node("chhetrapati", parent=kathmandu)
dallu = Node("dallu", parent=kathmandu)
jhamsikhel = Node("jhamsikhel", parent=kathmandu)
jawalakhel = Node("jawalakhel", parent=kathmandu)
dakchhinkali = Node("dakchhinkali", parent=kathmandu)
khusibun = Node("khusibun", parent=kathmandu)
tengal = Node("tengal", parent=kathmandu)
bishal_bazar = Node("bishal bazar", parent=kathmandu)
sundhara = Node("sundhara", parent=kathmandu)
khichapokhari = Node("khichapokhari", parent=kathmandu)
bhadrakali = Node("bhadrakali", parent=kathmandu)
shreenagar = Node("shreenagar", parent=kathmandu)
jyatha = Node("jyatha", parent=kathmandu)
pakanajol = Node("pakanajol", parent=kathmandu)
dhobichaur = Node("dhobichaur", parent=kathmandu)
siddhitol = Node("siddhitol", parent=kathmandu)
pragatinagar = Node("pragatinagar", parent=kathmandu)
lokanthali = Node("lokanthali", parent=kathmandu)
kausaltar = Node("kausaltar", parent=bhaktapur)
gatthaghar = Node("gatthaghar", parent=bhaktapur)
thimi = Node("thimi", parent=bhaktapur)
changunarayan = Node("changunarayan", parent=bhaktapur)


class LocationInformation:

    def all_ktm_locations(self):
        for row in RenderTree(kathmandu):
            if row.node.parent == kathmandu:
                ktm_locations.append(row.node.name)
        return ktm_locations

    def all_ltp_locations(self):
        for row in RenderTree(lalitpur):
            if row.node.parent == lalitpur:
                ltp_locations.append(row.node.name)
        return ltp_locations

    def all_bkt_locations(self):
        for row in RenderTree(bhaktapur):
            if row.node.parent == bhaktapur:
                bkt_locations.append(row.node.name)
        return bkt_locations

    def all_locations(self):
        for row in RenderTree(nepal):
            if row.node.parent == nepal:
                outside_locations.append(row.node.name)
        return outside_locations

# print (RenderTree(nepal))