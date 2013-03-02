# Maintainer : Andrew Clunis <andrew@orospakr.ca>

pkgname=vrms
pkgver=20130302
pkgrel=1
pkgdesc="vrms for ArchLinux"
arch=('any')
url="https://github.com/orospakr/vrms-arch"
license=('custom: BSD3')
depends=('python>=3.3' 'pyalpm>=0.5.3')
source=()
md5sums=()

_gitname=vrms-arch
_gitroot=git://github.com/orospakr/vrms-arch

build() {
  cd ${srcdir}
  msg "Fetching stable branch from git..."
  if [[ -d "$_gitname" ]]; then
    cd "$_gitname" && git fetch origin && git merge --ff-only origin/stable
    msg "The local files are updated."
  else
    git clone "$_gitroot" "$_gitname" -b stable
  fi

  # I don't like this "or"
  msg "Checkout from git done, or server timeout."
  msg "Starting build..."

  # on Pacman 4, it is recommended to make a separate copy of the
  # source to build from when using a VCS

  rm -rf "$srcdir/$_gitname-build"
  cp -R "$srcdir/$_gitname" "$srcdir/$_gitname-build"
  cd "$srcdir/$_gitname-build"

  python setup.py build
}

package() {
  cd "$srcdir/$_gitname-build"
  python setup.py install --root=${pkgdir}
}
