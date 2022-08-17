import os
import sys

def main():
    versions = []
    tasks = []
    
    args = sys.argv
    
    for i in range(1, len(args)):
        arg = args[i]
        
        if is_minecraft_version(arg):
            versions.append(arg)
        elif is_gradle_task(arg):
            tasks.append(arg)
        else:
            raise Exception("unrecognized arg " + arg + "!")
    
    if len(versions) == 0:
        if 'MC_VERSION' in os.environ:
            version = os.environ['MC_VERSION']
            
            if is_minecraft_version(version):
                versions.append(version)
            else:
                raise Exception("no minecraft version given!")
        else:
            find_minecraft_versions(versions)
    if len(tasks) == 0:
        raise Exception("no gradle tasks given!")
    
    command = "gradlew" if os.name == "nt" else "./gradlew"
    command += " " + " ".join(tasks)
    
    for version in versions:
        os.environ['MC_VERSION'] = version
        os.system(command)

def is_minecraft_version(string):
    return string == "1.7.2"

def is_gradle_task(string):
    return string == "build"

def find_minecraft_versions(versions):
    versions.append("1.7.2")

if __name__ == '__main__':
    main()
