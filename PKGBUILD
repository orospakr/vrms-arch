# Maintainer : Andrew Clunis <andrew@orospakr.ca>
# Contributor: Ben R <thebenj88 *AT* gmail *DOT* com>

pkgname=vrms-arch
pkgver=20130302
pkgrel=1
pkgdesc="vrms for ArchLinux"
arch=('any')
url="https://github.com/orospakr/${pkgname}"
license=('custom:BSD3')
depends=('python' 'pyalpm')
source=("git+https://github.com/orospakr/${pkgname}.git")
md5sums=('SKIP')

build() {
  cd "$srcdir/${pkgname}"
  python setup.py build
}

package() {
  cd "$srcdir/${pkgname}"
  python setup.py install --root=${pkgdir}
  install -Dm 644 COPYING "${pkgdir}/usr/share/license/${pkgname}/LICENSE"
}