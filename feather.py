import os
import sys

MAPPINGS_DIR = "mappings"
GRADLE_TASKS = ["feather", "build", "javadoc", "javadocJar", "checkMappings", "mapNamedJar"]
GRADLEW = "gradlew" if os.name == "nt" else "./gradlew"

def main():
    versions = []
    tasks = []
    
    args = sys.argv
    
    for i in range(1, len(args)):
        arg = args[i]
        
        if is_minecraft_version(arg):
            versions.append(arg)
        elif arg in GRADLE_TASKS:
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
    
    command = GRADLEW + " " + " ".join(tasks) + " --stacktrace"
    
    for version in versions:
        os.environ['MC_VERSION'] = version
        os.system(command)

def is_minecraft_version(string):
    path = os.path.join(MAPPINGS_DIR, string)
    return os.path.isdir(path)

def find_minecraft_versions(versions):
    for version in os.listdir(MAPPINGS_DIR):
        path = os.path.join(MAPPINGS_DIR, version)
        
        if os.path.isdir(path):
            versions.append(version)

if __name__ == '__main__':
    main()
