import pyalpm
import re
import sys

def clean_license_name(license):
    license = license.lower()
    license = re.sub('(?:^custom:|[,\s_"-])', '', license)
    return license

AMBIGUOUS_LICENSES = [clean_license_name(license) for license in [
    "custom",
    "other",
    "unknown",
    # CCPL (Creative Commons) should be specified with one of the
    # sublicenses (one of /usr/share/licenses/common/CCPL/*) , some of
    # which are non-free
    "CCPL", # ['claws-mail-themes', '0ad', '0ad-data', 'archlinux-lxdm-theme', 'mari0', 'performous-freesongs']
    "CCPL:cc-by-sa-3.0",
]]

FREE_LICENSES = [clean_license_name(license) for license in [
    'AFL-3.0',
    'AGPL',
    'AGPL3',
    'Apache',
    'Apache 2.0',
    'Apache 2.0 with LLVM Exception',
    'Apache 2.0 with LLVM Execption',
    'Apache License (2.0)',
    'Apache2',
    'Arphic Public License',
    'Artistic',
    'Artistic 2.0',
    'Beerware',
    'bitstream-vera',
    'Boost',
    'BSD',
    'BSD2',
    'BSD-2-clause',
    'BSD3',
    'BSD-3-clause',
    'BSD-like',
    'BSD-style',
    'BSL',
    'bzip2',
    'CC0',
    'CCBYSA',
    'cc-by-sa-2.5',
    'CCBYSA3.0',
    'CC BY-SA 4.0',
    'CCPL:by-sa',
    'CCPL:cc-by-sa',
    'CDDL',
    'CeCILL',
    'CPL',
    'Creative Commons, Attribution 3.0 Unported',
    'dumb',
    'EDL',
    'EPL',
    'EPL/1.1',
    'etpan',
    'ex',
    'Expat',
    'FDL',
    'FDL1.2',
    'FFSL',
    'FIPL',
    'font embedding exception',
    'GD',
    'GFL',
    'GPL',
    'GPL2',
    'GPL-2.0+',
    'GPL-2.0',
    'GPL3',
    'GPL-3.0',
    'GPL3+GPLv2',
    'GPL3-only',
    'GPL3 or any later version',
    'GPL/BSD',
    'GPL+FE',
    'GPLv2',
    'GPLv3',
    'HPND',
    'IBM Public Licence',
    'icu',
    'Info-ZIP',
    'INN',
    'ISC',
    'isc-dhcp',
    'JasPer2.0',
    'Khronos',
    'LGPL',
    'LGPL2',
    'LGPL2.1',
    'LGPL2.1+',
    'LGPL3',
    'LGPLv3+',
    'libpng',
    'libtiff',
    'libxcomposite',
    'LPPL',
    'lsof',
    'MirOS',
    'MIT',
    'MIT/X',
    'MITX11',
    'MIT-style',
    'Modified BSD',
    'MPL',
    'MPL2',
    'MPLv2',
    'NCSA',
    'neovim',
    'nfsidmap',
    'NoCopyright',
    'none',
    'OASIS',
    'OFL',
    'OFL-1.1',
    'OPEN DATA LICENSE',
    'OpenLDAP',
    'OpenMPI',
    'OSGPL',
    'perl',
    'PerlArtistic',
    'PerlArtistic2',
    'PHP',
    'pil',
    'PostgreSQL',
    'PSF',
    'Public Domain',
    'Python',
    'Qhull',
    'QPL',
    'QPL-1.0',
    'qwt',
    'Ruby',
    'scite',
    'scowl',
    'Sendmail',
    'Sendmail open source license',
    'SGI',
    'SIL',
    'SIL Open Font License',
    'SIL Open Font License 1.1 and Bitstream Vera License',
    'SIL Open Font License, Version 1.0',
    'SIL OPEN FONT LICENSE Version 1.1',
    'sip',
    'Sleepycat',
    'tcl',
    'TekHVC',
    'TRADEMARKS',
    'Ubuntu Font Licence 1.0',
    'UCD',
    'Unicode-DFS',
    'University of Illinois/NCSA Open Source License',
    'Unlicense',
    'usermin',
    'vim',
    'voidspace',
    'W3C',
    'w3m',
    'webmin',
    'WTF',
    'WTFPL',
    'wxWindows',
    'X11',
    'X11-DEC',
    'XFREE86',
    'Xiph',
    'zlib',
    'zlib/libpng',
    'ZPL',
]]

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
            licenses = [clean_license_name(license) for license in pkg.licenses]
            for license in licenses:
                # get a list of all licenses on the box
                if license not in self.by_license:
                    self.by_license[license] = [pkg]
                else:
                    self.by_license[license].append(pkg)

            free_licenses = list(filter(lambda x: x in FREE_LICENSES, licenses))
            amb_licenses = list(filter(lambda x: x in AMBIGUOUS_LICENSES, licenses))

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
