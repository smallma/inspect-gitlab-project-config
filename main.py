#!/usr/bin/env python
import os
import json
import sys

GitRootPath = '/var/opt/gitlab/git-data/repositories/WD/'
GitConfigTempFile = '/mnt/tools/inspectGit/temp_project'
ProjectInfoFile = '/mnt/share/05-WebServer/project/inspectProjectInfo/project_info.json'
projectInfo = {}


def recordProjectInfo(jsonData):
  open(ProjectInfoFile, 'w').close()

  with open(ProjectInfoFile, 'w') as f:
    json.dump(jsonData, f)

def getJsonValue(jsonData, key):
  try:
    return jsonData[key]
  except Exception as e:
    return ''

def getTempProjectConfig(projectName):
  with open(GitConfigTempFile) as jsonFile:
    try:
      data = json.load(jsonFile)

      default = data['default']
      hashId = getJsonValue(default, 'hashId')
      productType = getJsonValue(default, 'productType')
      mdeiaId = getJsonValue(default, 'productType')
      productId = getJsonValue(default, 'productId')
      pageType = getJsonValue(default, 'pageType')

      info = {
        'productType': productType,
        'mdeiaId': mdeiaId,
        'productId': productId,
        'pageType': pageType,
     	'hashId': hashId
      }

      print info
      projectInfo[projectName] = info

      if not projectInfo[projectName]:
        projectInfo[projectName] = info
      else:
        projectNameNew = projectName + '_duplicate'
        projectInfo[projectNameNew] = info

    except Exception as e:
     return

def getGitGulpConfig(projectName):
  projectPath = os.path.join(GitRootPath, projectName)
  if not os.path.exists(projectPath):
    return

  os.chdir(projectPath)
  os.system('git show master:gulpEnv/config.json > /mnt/tools/inspectGit/temp_project')
  getTempProjectConfig(projectName)


def getGitProjectNames(gitRecords):
  projectNames = []
  for line in gitRecords:
    projectName = line.split()[-1]
    if not projectName.endswith('.wiki.git'):
      projectNames.append(projectName)
  return projectNames


def parsingGits():
  with open('gits', 'r') as f:
    gitRecords = [line.strip() for line in f]
    return gitRecords


def recordGits():
  os.popen("sudo -S ls -l /var/opt/gitlab/git-data/repositories/WD/ | grep '^d' > gits", 'w').write("PWD")


def main():
  recordGits()
  gitRecords = parsingGits()
  projectNames = getGitProjectNames(gitRecords)

  for projectName in projectNames:
    getGitGulpConfig(projectName)

  print projectInfo
  recordProjectInfo(projectInfo)

  
if __name__ == '__main__':
  main()
