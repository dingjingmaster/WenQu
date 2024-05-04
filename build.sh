#!/bin/bash
set -e

versionMajor=0
versionMinor=2
versionPatch=0
versionTweak=0
version="${versionMajor}.${versionMinor}.${versionPatch}.${versionTweak}"

packageMD5=""
# shellcheck disable=SC2046
curDir=$(dirname $(realpath -- "$0"))
workDir=${curDir}/out
packageName="WenQu-${version}.tar.gz"

sed -i -E "s/^version\ =\ \"[0-9].[0-9].[0-9].[0-9]\"/version\ =\ \"${version}\"/" "${curDir}/pyproject.toml"

[[ -d "${workDir}" ]] && rm -rf "${workDir}"
[[ ! -d "${workDir}" ]] && mkdir -p "${workDir}"

tar cf "${packageName}" ./docs ./tests ./data ./app ./main.py ./poetry.lock ./pyproject.toml ./LICENSE ./README.md
[[ -f "./${packageName}" ]] && mv "./${packageName}" "${workDir}"
[[ -f "${workDir}/${packageName}" ]] && packageMD5=$(sha512sum "${workDir}/${packageName}" | awk '{print $1}')


cat << EOF > ${workDir}/PKGBUILD
# Maintainer: dingjing <dingjing@live.cn>

pkgname=wenqu
pkgver=${versionMajor}.${versionMinor}.${versionPatch}
pkgrel=${versionTweak}
pkgdesc='AI 助手.'
url='https://github.com/dingjingmaster/WenQu'
arch=('any')
license=('MIT')
depends=('poetry' 'ollama' 'gnome-terminal')
optdepends=()
makedepends=('fakeroot' 'debugedit')
source=("${workDir}/${packageName}")

sha512sums=("${packageMD5}")
noextract=()
validpgpkeys=('18B65970A361B77D6C7C67C29EE375D12E7A3EB1')

#prepare() {
#  cd \$pkgname-\$pkgver
#}

#build() {
#  cd \$pkgname-\$pkgver
#}

package() {
  install -dTm 0755 \${pkgdir}/opt/WenQu/
  install -dTm 0755 \${pkgdir}/opt/WenQu/app
  install -Dm  0755 \${srcdir}/main.py              \${pkgdir}/opt/WenQu/main.py
  install -Dm  0755 \${srcdir}/LICENSE              \${pkgdir}/opt/WenQu/LICENSE
  install -Dm  0755 \${srcdir}/README.md            \${pkgdir}/opt/WenQu/README.md
  install -Dm  0744 \${srcdir}/poetry.lock          \${pkgdir}/opt/WenQu/poetry.lock
  install -Dm  0744 \${srcdir}/pyproject.toml       \${pkgdir}/opt/WenQu/pyproject.toml
  install -Dm  0755 \${srcdir}/data/WenQu.svg       \${pkgdir}/opt/WenQu/data/WenQu.svg
  install -Dm  0644 \${srcdir}/data/WenQu.desktop   \${pkgdir}/usr/share/applications/WenQu.desktop

  cp -afr \${srcdir}/app/* \${pkgdir}/opt/WenQu/app
  chmod 0655 -R \${pkgdir}/opt/WenQu/app
}

post_install() {
    systemctl start ollama
    systemctl enable ollama
    ollama pull llama3:instruct
}

pre_remove() {
    systemctl stop ollama
    systemctl disable ollama
}

EOF

cd "${workDir}"
makepkg --printsrcinfo > .SRCINFO
makepkg
cd "${curDir}"