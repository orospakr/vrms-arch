import pyalpm
import sys

AMBIGUOUS_LICENSES = [
    "custom",
    "other",
    "unknown",
    "CUSTOM",
    # CCPL (Creative Commons) should be specified with one of the
    # sublicenses (one of /usr/share/licenses/common/CCPL/*) , some of
    # which are non-free
    "CCPL", # ['claws-mail-themes', '0ad', '0ad-data', 'archlinux-lxdm-theme', 'mari0', 'performous-freesongs']
    "CCPL:cc-by-sa-3.0",
]

FREE_LICENSES = [
    'AGPL',
    'AGPL3',
    'APACHE',
    'Apache',
    'Apache 2.0',
    'Apache License (2.0)',
    'apache',
    'Artistic',
    'Artistic2.0',
    'Boost',
    'boost',
    'BSD',
    'bsd',
    'BSD2',
    'BSD-2',
    'BSD3',
    'CC0',
    'CC BY-SA 4.0',
    'CC-BY-SA 4.0',
    'CCPL:by-sa',
    'CCPL:cc-by-sa',
    'CDDL',
    'CPL',
    'EPL',
    'EPL/1.1',
    'FDL',
    'FDL1.2',
    'GPL',
    'GPL-2'
    'GPL-2.0',
    'GPL-2.0+',
    'GPL-3',
    'GPL-3.0',
    'GPL2',
    'GPL3',
    'GPL3-only',
    'GPL3+GPLv2',
    'GPLv2',
    'GPLv3',
    'GPL3 or any later version',
    'ISC',
    'LGPL',
    'LGPL2',
    'LGPL2.1',
    'LGPL3',
    'LGPLv3+',
    'MIT',
    'MPL',
    'MPL2',
    'Modified BSD',
    'OFL',
    'OFL-1.1',
    'PHP',
    'PSF',
    'perl',
    'PerlArtistic',
    'PerlArtistic2',
    'Public Domain',
    'Python',
    'RUBY',
    'Ruby',
    'SIL',
    'SIL OPEN FONT LICENSE Version 1.1',
    'SIL Open Font License 1.1 and Bitstream Vera License',
    'W3C',
    'WTFPL',
    'X11',
    'ZLIB',
    'zlib',
    'ZPL',
    'custom: Arphic Public_License',
    'custom: BSD',
    'custom: ISC',
    'custom: MIT',
    'custom: OFL',
    'custom: SIL Open Font License',
    'custom: QPL-1.0',
    'custom: public domain',
    'custom:"IBM Public Licence"',
    'custom:"font embedding exception"',
    'custom:"icu"',
    'custom:"pil"',
    'custom:"sip"',
    'custom:Arphic Public License',
    'custom:Arphic_Public_License',
    'custom:Artistic',
    'custom:Artistic 2.0',
    'custom:Artistic-2.0',
    'custom:Apache 2.0 with LLVM Exception',
    'custom:Apache 2.0 with LLVM Execption',
    'custom:BSD',
    'custom:BSD-like',
    'custom:BSD-style',
    'custom:BSD2',
    'custom:BSD3',
    'custom:Boost',
    'custom:CC0',
    'custom:CCBYSA',
    'custom:CCBYSA3.0',
    'custom:CCPL:by-sa',
    'custom:CeCILL',
    'custom:Creative Commons, Attribution 3.0 Unported',
    'custom:EPL',
    'custom:Expat',
    'custom:FFSL',
    'custom:FIPL',
    'custom:GD',
    'custom:GFL',
    'custom:GPL',
    'custom:GPL/BSD',
    'custom:GPL+FE',
    'custom:HPND',
    'custom:INN',
    'custom:Info-ZIP',
    'custom:ISC',
    'custom:JasPer2.0',
    'custom:Khronos',
    'custom:LGPL',
    'custom:LGPL2',
    'custom:MIT',
    'custom:MIT/X',
    'custom:MITX11',
    'custom:MPL2',
    'custom:MPLv2',
    'custom:MirOS',
    'custom:NoCopyright',
    'custom:OASIS',
    'custom:OFL',
    'custom:OPEN DATA LICENSE',
    'custom:OpenLDAP',
    'custom:OpenMPI',
    'custom:OSGPL',
    'custom:PYTHON',
    'custom:PostgreSQL',
    'custom:PSF',
    'custom:Public Domain',
    'custom:Public_Domain',
    'custom:PublicDomain',
    'custom:QPL',
    'custom:Qhull',
    'custom:SGI',
    'custom:SIL',
    'custom:SIL Open Font License, Version 1.0',
    'custom:Sendmail',
    'custom:Sendmail open source license',
    'custom:Sleepycat',
    'custom:TekHVC',
    'custom:TRADEMARKS',
    'custom:Ubuntu Font Licence 1.0',
    'custom:University of Illinois/NCSA Open Source License',
    'custom:Unlicense',
    'custom:WTFPL',
    'custom:X11',
    'custom:X11-DEC',
    'custom:XFREE86',
    'custom:Xiph',
    'custom:ZLIB',
    'custom:artistic',
    'custom:bitstream-vera',
    'custom:bzip2',
    'custom:cc-by-sa-2.5',
    'custom:dumb',
    'custom:etpan',
    'custom:ex',
    'custom:icu',
    'custom:isc-dhcp',
    'custom:libpng',
    'custom:libtiff',
    'custom:libxcomposite',
    'custom:lsof',
    'custom:nfsidmap',
    'custom:neovim',
    'custom:none',
    'custom:public domain',
    'custom:publicdomain',
    'custom:qwt',
    'custom:scite',
    'custom:scowl',
    'custom:tcl',
    'custom:unknown',
    'custom:unlicense',
    'custom:usermin',
    'custom:vim',
    'custom:voidspace',
    'custom:w3m',
    'custom:webmin',
    'custom:wxWindows',
    'custom:zlib',
    'custom:zlib/libpng',
]

class LicenseFinder(object):
    def __init__(self):
        # all of the seen license names with counts
        self.by_license = {}

        # packages with "custom" license
        self.unknown_packages = set()

        # packages with a known non-free license
        self.nonfree_packages = set()

    def visit_db(self, db):
        pkgs = db.packages

        free_pkgs = []

        for pkg in pkgs:
            for license in pkg.licenses:
                # get a list of all licenses on the box
                if license not in self.by_license:
                    self.by_license[license] = [pkg]
                else:
                    self.by_license[license].append(pkg)

            free_licenses = list(filter(lambda x: x in FREE_LICENSES, pkg.licenses))
            amb_licenses = list(filter(lambda x: x in AMBIGUOUS_LICENSES, pkg.licenses))

            if len(free_licenses) > 0:
                free_pkgs.append(pkg)
                continue
            elif len(amb_licenses) > 0:
                self.unknown_packages.add(pkg)
            else:
                self.nonfree_packages.add(pkg)

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
