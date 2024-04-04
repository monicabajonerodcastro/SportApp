#!/bin/bash

VERSION=""

# Obtener parámetros
while getopts v: flag
do
  case "${flag}" in
    v) VERSION=${OPTARG};;
  esac
done

# Obtener el número de tag más alto, agregar v.1.0.0 si no existe ninguno
git fetch --prune --unshallow 2>/dev/null
CURRENT_VERSION=`git describe --tags $(git rev-list --tags --max-count=1) 2>/dev/null`

if [[ $CURRENT_VERSION == '' ]]
then
  CURRENT_VERSION='v1.0.0'
fi
echo "Version actual: $CURRENT_VERSION"

# Reemplazar . con espacio para convertirlo en array
CURRENT_VERSION_PARTS=(${CURRENT_VERSION//./ })

# Obtener cada número de version
VNUM1=${CURRENT_VERSION_PARTS[0]}
VNUM2=${CURRENT_VERSION_PARTS[1]}
VNUM3=${CURRENT_VERSION_PARTS[2]}

VNUM1=${CURRENT_VERSION_PARTS[0]}
VNUM2=${CURRENT_VERSION_PARTS[1]}
VNUM3=${CURRENT_VERSION_PARTS[2]}

if [[ $VERSION == 'major' ]]
then
  VNUM1=v$((VNUM1+1))
elif [[ $VERSION == 'minor' ]]
then
  VNUM2=$((VNUM2+1))
elif [[ $VERSION == 'patch' ]]
then
  VNUM3=$((VNUM3+1))
else
  echo "No se especificó ninguna version"
  exit 1
fi

# Se crea el nuevo tag
NEW_TAG="$VNUM1.$VNUM2.$VNUM3"
echo "($VERSION) updating $CURRENT_VERSION to $NEW_TAG"

# Obtener el hash actual y revisar si ya tiene una versión
GIT_COMMIT=`git rev-parse HEAD`
NEEDS_TAG=`git describe --contains $GIT_COMMIT 2>/dev/null`

if [ -z "$NEEDS_TAG" ]; then
  echo "Tagged with $NEW_TAG"
  git tag $NEW_TAG
  git push --tags
  git push
else
  echo "Already a tag on this commit"
fi

# Declarar variable de salida
echo ::set-output name=git-tag::$NEW_TAG

exit 0
exit 0
