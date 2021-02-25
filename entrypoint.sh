#!/usr/bin/env bash


set -e

PLAIN='\033[0m'
BOLD='\033[1;37m'

python3 -m pip install -r requirements.txt
python3 dojo.py
result=$?
if [ $result -eq 10 ]; then
  if [ "$GITHUB_EVENT_NAME" = "schedule" ]; then
    exit 0
  fi
fi


if [ "${INPUT_HUGOVERSION}" ]; then
  echo -e "\n${BOLD}Using Hugo version ${INPUT_HUGOVERSION}.${PLAIN}"
  wget "https://github.com/gohugoio/hugo/releases/download/v$(echo "${INPUT_HUGOVERSION}" | grep -o  "[0-9]\+.[0-9]\+.[0-9]\+")/hugo_${INPUT_HUGOVERSION}_Linux-64bit.tar.gz"
  /bin/tar -xzvf hugo*.tar.gz
  mv hugo /usr/bin/hugo
  rm hugo*
else
  echo -e "No Hugo version specified!"
  exit 1
fi

if [ "${INPUT_CNAME}" ]; then
  NAME=${INPUT_CNAME}
else
  NAME=${GITHUB_REPOSITORY}
fi

if [ "${INPUT_REPO}" ]; then
  REPO=${INPUT_REPO}
else
  REPO=${GITHUB_REPOSITORY}
fi

[ -z "${INPUT_GITHUBTOKEN}" ] && \
  (echo -e "\n${BOLD}ERROR: Missing githubToken.${PLAIN}" ; exit 1)


echo -e "\n${BOLD}Versions:${PLAIN}"
echo -ne "${BOLD}Hugo: ${PLAIN}"
hugo version

echo -e "\n${BOLD}Setting up Git${PLAIN}"
git config --global user.name "${GITHUB_ACTOR}"
git config --global user.email "${GITHUB_ACTOR}@users.noreply.github.com"
echo "machine github.com login ${GITHUB_ACTOR} password ${INPUT_GITHUBTOKEN}" > ~/.netrc

echo -e "\n${BOLD}Checking out instructions${PLAIN}"
while IFS=" " read -r p || [ -n "$p" ]
do
  INSTRUCTIE_REPO="${p% *}"
  INSTRUCTIE_PATH="${p#* }"
  git clone --depth=1 --single-branch https://x-access-token:${INPUT_GITHUBTOKEN}@github.com/$INSTRUCTIE_REPO.git $INSTRUCTIE_PATH
done < instructies.txt


echo -e "\n${BOLD}Generating Public Site ${NAME} at commit ${GITHUB_SHA}${PLAIN}"
git clone --depth=1 --single-branch --branch "gh-pages" "https://x-access-token:${INPUT_GITHUBTOKEN}@github.com/${REPO}.git" /tmp/gh-pages
rm -rf /tmp/gh-pages/*

hugo ${INPUT_ARGS} -d /tmp/gh-pages/

echo -e "\n${BOLD}Commiting${PLAIN}"
pushd /tmp/gh-pages

[ -n "${INPUT_CNAME}" ] && \
  echo "${INPUT_CNAME}" > CNAME

git add -A && git commit --allow-empty -am "Publishing Site ${NAME} at ${GITHUB_SHA} on $(date -u)"

echo -e "\n${BOLD}Pushing${PLAIN}"
git push --force
popd
echo -e "\n${BOLD}Site ${NAME} at ${GITHUB_SHA} was successfully deployed to ${INPUT_CNAME}!${PLAIN}"



echo -e "\n${BOLD}Generating MCS Site ${NAME} at commit ${GITHUB_SHA}${PLAIN}"
git clone --depth=1 --single-branch --branch "mcs" "https://x-access-token:${INPUT_GITHUBTOKEN}@github.com/${REPO}.git" /tmp/mcs
rm -rf /tmp/mcs/*

hugo ${INPUT_ARGS} --config config-mcs.toml -d /tmp/mcs/

echo -e "\n${BOLD}Commiting${PLAIN}"
pushd /tmp/mcs

git add -A && git commit --allow-empty -am "Publishing Site ${NAME} at ${GITHUB_SHA} on $(date -u)"

echo -e "\n${BOLD}Pushing${PLAIN}"
git push --force
popd
echo -e "\n${BOLD}Site ${NAME} at ${GITHUB_SHA} was successfully deployed MCS branch!${PLAIN}"
