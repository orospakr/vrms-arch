import pyalpm
import sys

AMBIGUOUS_LICENSES = [
    "custom",
    "other",
    "unknown",
    # CCPL (Creative Commons) should be specified with one of the
    # sublicenses (one of /usr/share/licenses/common/CCPL/*) , some of
    # which are non-free
    "CCPL", # ['claws-mail-themes', '0ad', '0ad-data', 'archlinux-lxdm-theme', 'mari0', 'performous-freesongs']
]

FREE_LICENSES = [
    "GPL",
    "LGPL",
    "GPL2",
    "PerlArtistic",
    "BSD",
    "FDL",
    "GPL3",
    "MIT",
    "MPL",
    "APACHE",
    "LGPL2.1",
    "LGPL3",
    "custom:BSD3",
    "custom:BSD",
    "PHP",
    "custom:MIT",
    "FDL1.2",
    "Apache",
    "ZLIB",
    "PSF",
    "custom:vim",
    "custom:ISC",
    "custom:LGPL",
    "custom:University of Illinois/NCSA Open Source License",
    "Artistic",
    "LGPL2", # ['mono', 'ocaml', 'taglib-sharp', 'omniorb', 'pyogg', 'lib32-gdk-pixbuf2']
    "zlib", # ['box2d', 'clanlib', 'csfml', 'love', 'sfml', 'tinyxml']
    "custom:OFL", # ['ttf-linux-libertine', 'terminus-font', 'ttf-gentium', 'ttf-inconsolata', 'ttf-liberation']
    "custom: MIT", # ['hardlink', 'newsbeuter', 'python-sqlalchemy', 'python2-sqlalchemy']
    "ZPL", # ['python-zope-interface', 'python2-zope-interface', 'python2-mechanize', 'python2-meld3']
    "custom:PostgreSQL", # ['postgresql', 'postgresql-docs', 'postgresql-libs', 'postgresql-old-upgrade']
    "AGPL", # ['ghostscript', 'itext', 'esmska', 'python2-ubuntuone-storageprotocol']
    "apache", # ['intellij-idea-community-edition', 'intellij-idea-libs', 'jmeter', 'ttf-droid']
    "custom:PYTHON", # ['python-dateutil', 'python-pyserial', 'python2-dateutil', 'python2-pyserial']
    "custom:\"font embedding exception\"", # ['wqy-bitmapfont', 'wqy-microhei', 'wqy-zenhei']
    "custom:zlib", # ['qwtplot3d', 'bullet', 'bullet-docs']
    "custom: ISC", # ['python-requests', 'python2-grequests', 'python2-requests']
    "CDDL", # ['cdrtools', 'libraw', 'netbeans']
    "EPL", # ['eclipse-ecj', 'swt', 'eclipse-cdt']
    "custom: BSD", # ['python-psutil', 'python2-psutil', 'sfk']
    "custom:CeCILL", # ['gimp-plugin-gmic', 'gmic', 'zart'] # FSF approves, OSI does not!
    "CPL", # ['junit', 'clojure', 'sleuthkit']
    "custom:wxWindows", # ['wxgtk', 'wxpython', 'wxgtk2.9']
    "Modified BSD", # ['ipython', 'ipython2', 'ipython2-docs']
    "CUSTOM", # ['vde2', 'python2-lcms', 'python2-reportlab']
    "custom:unknown", # ['perl-guard', 'erlang-cl']
    "CCPL:cc-by-sa", # ['archlinux-themes-kdm', 'archlinux-themes-slim']
    "Public Domain", # ['stopwatch', 'unclutter']
    "custom:cc-by-sa-2.5", # ['human-icon-theme', 'tangerine-icon-theme']
    "custom:isc-dhcp", # ['dhclient', 'dhcp']
    "custom:Expat", # ['pep8-python2', 'pep8-python3']
    "custom:WTFPL", # ['ponysay', 'vim-nerdtree'] # FSF approves, OSI does not!
    "custom:zlib/libpng", # ['liblinebreak', 'ois']
    "custom: QPL-1.0", # ['ocaml', 'ocaml-compiler-libs']
    "custom:ZLIB", # ['glfw', 'libharu']
    "custom:Creative Commons, Attribution 3.0 Unported", # ['mythes-nl', 'hunspell-nl']
    "custom:MIT/X", # ['tabbed']
    "custom:MPLv2", # ['hunspell-fr']
    "custom:etpan", # ['libetpan']
    "custom:INN", # ['inn']
    "custom:Artistic", # ['procmail']
    "Artistic2.0", # ['simutrans-pak128']
    "custom:ex", # ['vi']
    "custom:XFREE86", # ['lib32-libx11']
    "custom:MirOS", # ['kwalletcli']
    "custom:GPL", # ['faad2']
    # "custom:Sendmail open source license", ['libmilter']
                                              # technically if only
                                              # Sendmail Inc/Eric
                                              # Allman is copyright
                                              # holder. too hard to
                                              # figure out this one.
                                              # maybe this is why
                                              # debian used exim ;)

    "PerlArtistic2", # ['perl-module-implementation']
    "custom:Artistic 2.0", # ['pv']
    "RUBY", # ['ruby-highline']
    "Python", # ['python2-memcached']
    "custom:Arphic Public License", # ['opendesktop-fonts']
    "custom:PUEL", # ['virtualbox-guest-iso']
    "custom:scite", # ['scite']
    "custom:Arphic_Public_License", # ['ttf-arphic-uming']
    "custom:Boost", # ['pion']
    "custom:GPL/BSD", # ['ppp']
    "custom:voidspace", # ['python2-configobj']
    "custom:BSD-style", # ['javasqlite']
    "custom:MITX11", # ['mono']
    "custom:QPL", # ['qt3-doc']
    "custom:icu", # ['lib32-icu']
    "custom:scowl", # ['hunspell-en']
    "custom:EPL", # ['graphviz']
    "BSD3", # ['haskell-bytestring-show']
    "custom:Artistic-2.0", # ['qpdf']
    "custom:publicdomain", # ['spring-kp']
    "custom:\"pil\"", # ['python2-imaging']
    "custom:\"IBM Public Licence\"", # ['sleuthkit']
    "custom:FIPL", # ['freeimage']
    "custom:\"icu\"", # ['icu']
    "custom:qwt", # ['qwt']
    "custom:NoCopyright", # ['dnssec-anchors'] # public domain?
    "custom:webmin", # ['webmin']
    "custom:CCBYSA3.0", # ['megaglest-data']
    "custom:Sendmail", # ['opendkim']
    "custom:CCPL:by-sa", # ['openstreetmap-map-icons-svn']
    "custom:TRADEMARKS", # ['archlinux-artwork']
    "W3C", # ['libwww']
    "custom:usermin", # ['usermin']
    "custom:Ubuntu Font Licence 1.0", # ['ttf-ubuntu-font-family'] #
                                      # derivative of SIL, going to
                                      # assume yes
    "custom:OASIS", # ['hunspell-de']
    "perl", # ['perl-module-runtime']
    "custom:artistic", # ['chromium-bsu']
    "bsd", # ['tcllib']
    "custom:nfsidmap", # ['nfsidmap']
    "custom:LGPL2", # ['sk1libs']
    "custom:none", # ['licenses'] # public domain?
    "AGPL3", # ['mongodb']
    "custom:public domain", # ['python2-webpy']
    "custom:Xiph", # ['lib32-flac']
    "EPL/1.1", # ['eclipse']
    "custom:Public_Domain", # ['ttf-mph-2b-damase']
    "CCPL:by-sa", # ['geogebra']
    "custom:FFSL", # ['ttytter']
    "boost", # ['boost-build']
    "custom:Public Domain", # ['talkfilters']
    "custom:OPEN DATA LICENSE", # ['geoip-database']
    "custom:OSGPL", # ['openscenegraph']
    "custom:JasPer2.0", # ['jasper']
    "custom:dumb", # ['dumb']
    "ISC", # ['yajl']
    "custom:CCBYSA", # ['zaz']
    "custom: Arphic Public_License", # ['ttf-arphic-ukai']
    
    # and a few more goofy variants that I personally found on AUR:
    "GPL-3",
    "GPL3+"
]

FREE_LICENSES_NAMING_VARIANTS = [
    "GPLv2"
]

FREE_LICENSES += FREE_LICENSES_NAMING_VARIANTS

class LicenseFinder(object):
    def __init__(self):
        # all of the seen license names with counts
        self.by_license = {}

        # packages with "custom" license
        self.unknown_packages = []

        # packages with a known non-free license
        self.nonfree_packages = []

    def visit_db(self, db):
        pkgs = db.search("")

        for pkg in pkgs:
            for license in pkg.licenses:
                # get a list of all licenses on the box
                if license not in self.by_license:
                    self.by_license[license] = [pkg]
                else:
                    self.by_license[license].append(pkg)

                if license not in FREE_LICENSES:
                    if license in AMBIGUOUS_LICENSES:
                        if (pkg not in self.unknown_packages):
                            self.unknown_packages.append(pkg)
                    else:
                        if (pkg not in self.nonfree_packages):
                            self.nonfree_packages.append(pkg)

    # Print all seen licenses in a convenient almost python list
    def list_all_licenses_as_python(self):
        obscure_license_pop_cutoff = 7
        sorted_by_popularity = list(self.by_license.keys())
        sorted_by_popularity.sort(key=lambda lic : len(self.by_license[lic]), reverse=True)
        for lic in sorted_by_popularity:
            pop = len(self.by_license[lic])
            print("    \"%s\",%s" % (lic.replace("\"", "\\\""), " # %s" % [ p.name for p in self.by_license[lic] ] if pop < obscure_license_pop_cutoff else ""))

    def list_all_licenses(self):
        sorted_by_popularity = list(self.by_license.keys())
        sorted_by_popularity.sort(key=lambda lic : len(self.by_license[lic]), reverse=True)
        for lic in sorted_by_popularity:
            print("%s: %d" % (lic, len(self.by_license[lic])))

    def list_all_unknown_packages(self):
        print("Packages of unknown license on this system: %d" % len(self.unknown_packages), file=sys.stderr)

        for upackage in self.unknown_packages:
            print("%s: %s" % (upackage.name, upackage.licenses))

    def list_all_nonfree_packages(self):
        for nfpackage in self.nonfree_packages:
            print("%s: %s" % (nfpackage.name, nfpackage.licenses))

        print("\nNon-free packages: %d\n" % len(self.nonfree_packages), file=sys.stderr)

        print("However, there are %d ambiguously licensed packages that vrms cannot certify." % len(self.unknown_packages), file=sys.stderr)
