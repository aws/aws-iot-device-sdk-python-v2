#!/usr/bin/env bash

set -ex

# Redirect output to stderr.
exec 1>&2

GITHUB_TOKEN=$1
[ -n "$GITHUB_TOKEN" ]

TAG_PR_TOKEN=$2
[ -n "$TAG_PR_TOKEN" ]

pushd $(dirname $0) > /dev/null

git checkout main

version=$(git describe --tags --abbrev=0)
version_without_v=$(echo ${version} | cut -f2 -dv)
echo "${version_without_v}" > VERSION

if git diff --exit-code VERSION > /dev/null; then
    echo "No version change"
else
    version_branch=AutoTag-${version}
    git checkout -b ${version_branch}

    git config --local user.email "aws-sdk-common-runtime@amazon.com"
    git config --local user.name "GitHub Actions"
    git add VERSION
    git commit -m "Updated version to ${version}"

    echo $TAG_PR_TOKEN | gh auth login --with-token

    # awkward - we need to snip the old release message and then force overwrite the tag with the new commit but
    # preserving the old message
    # the release message seems to be best retrievable by grabbing the last lines of the release view from the
    # github cli
    release_line_count=$(gh release view ${version} | wc -l)
    let release_message_lines=release_line_count-8
    tag_message=$(gh release view ${version} | tail -n ${release_message_lines})
    title_line=$(gh release view ${version} | head -n 1)
    title_value=$(echo $title_line | sed -n "s/title: \(.*\)/\1/p")
    echo "Old release title is: ${title_value}"
    echo "Old release message is: ${tag_message}"

    # push the commit
    git push -u "https://${GITHUB_ACTOR}:${GITHUB_TOKEN}@github.com/aws/aws-iot-device-sdk-python-v2.git" ${version_branch}

    gh pr create --title "AutoTag PR for ${version}" --body "AutoTag PR for ${version}" --head ${version_branch}

    # this requires more permissions than the bot token currently has
    # todo: can we update the bot token so that my pat isn't necessary?
    gh pr merge --admin --squash

    # update local state with the merged pr
    git fetch
    git checkout main
    git pull "https://${GITHUB_ACTOR}:${GITHUB_TOKEN}@github.com/aws/aws-iot-device-sdk-python-v2.git" main

    # delete old release
    gh release delete -y ${version}

    # delete the old tag
    git tag -d ${version}
    git push "https://${GITHUB_ACTOR}:${GITHUB_TOKEN}@github.com/aws/aws-iot-device-sdk-python-v2.git" :refs/tags/${version}

    # create new tag on latest commit with old message
    git tag -f ${version} -m "${tag_message}"

    # push new tag to github
    git push "https://${GITHUB_ACTOR}:${GITHUB_TOKEN}@github.com/aws/aws-iot-device-sdk-python-v2.git" --tags

    # now recreate the release on the updated tag
    gh release create ${version} --title "${title_value}" -p -n "${tag_message}"
fi

popd > /dev/null
