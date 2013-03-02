# `vrms` for ArchLinux

Enumerates non-free packages (that is to say, under licenses not
considered by OSI, FSF, and/or the DFSG to be Free Software) installed
on an ArchLinux system.  See `vrms_arch/license_finder.py` for the
license categorization.

Copyright (C) 2013
Andrew Clunis <[andrew@orospakr.ca](mailto:andrew@orospakr.ca)>.

Released under the New 3-Clause BSD license (trololo!).  See
`COPYING`.

A reimplementation of the original
[`vrms`](http://vrms.alioth.debian.org/) program from Debian for
Arch's Pacman and ALPM.

# Usage

List non-free packages (and count currently ambiguous/uncheckable
packages, see Caveats)

    vrms
    
Check all packages in locally synced package repositories (does not
and can not include the AUR), not just locally installed packages:

    vrms -g

# Building

Build a package out of local checkout of this source code on Arch:

    makepkg --noextract
    
This works because I include a `src` symlink that points to `..`,
which fools `makepkg` into using the local checkout as the source.

The same PKGBUILD, without `--noextract` and the `src` symlink, will
fetch whatever's on the `stable` branch of the GitHub repo.

## Caveats

A great deal of packages in Arch, both free and non-free, use `custom`
as the license field value.  As per the
[Arch Packaging Standards](https://wiki.archlinux.org/index.php/Arch_Packaging_Standards#Licenses),
this indicates that the package does not use an exact copy of one of
the licenses included in the core
[`licenses` package](https://www.archlinux.org/packages/core/any/licenses/),
which provides well-known free licenses at
`/usr/share/licenses/common`.  However, the Packaging Standards go on
to say that the license field can be disambiguated in the form of
`custom: ZLIB` or `custom: PUEL`.  Sadly, there are 722 packages in
the ArchLinux pacman repositories (Core, Community, Extra, and
Multilib) that specify only `custom`.  Many packages also carelessly
use variant naming of well-known licenses (`GPL-2`, `GPLv2`, etc.) in
spite of the Packaging Standards, causing further confusion.

Many commonly used Free Software licenses aren't included in the
common `licenses` packages because they require editing to be applied
to a given project, such as the BSD and MIT licenses.

The same problems extend to the AUR.
