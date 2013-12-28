AMBIGUOUS_PACKAGES = {
    'flashplugin': ['custom:non-free']
}

class Package(object):
    def __init__(self, name, licenses):
        self.name = name
        self.licenses = licenses

class UnambiguousDb(object):
    def __init__(self, db):
        self.packages = []

        for pkg in db.search(""):
            if pkg.name in AMBIGUOUS_PACKAGES:
                self.packages.append(Package(pkg.name, AMBIGUOUS_PACKAGES[pkg.name]))
            else:
                self.packages.append(Package(pkg.name, pkg.licenses))
