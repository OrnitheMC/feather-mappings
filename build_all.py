import os
import sys
import subprocess

MAPPINGS_DIR = 'mappings'
GRADLEW = 'gradlew' if os.name == 'nt' else './gradlew'

# some jank to hide versions that are giving problems
UNAVAILABLE_VERSIONS = []

def main():
    versions = find_minecraft_versions()
    
    while versions:
        failed = []
        
        for version in versions:
            os.environ['MC_VERSION'] = version
            try:
                subprocess.run("{} build javadocJar checkMappings mapNamedJar --stacktrace".format(GRADLEW), shell = True, check = True)
            except subprocess.CalledProcessError:
                failed.append(version)
         
        versions = failed

def find_minecraft_versions():
    versions = []
    
    for filename in os.listdir(MAPPINGS_DIR):
        path = os.path.join(MAPPINGS_DIR, filename)
        
        if filename.endswith('.tiny'):
            versions.append(filename[0:len(filename) - len('.tiny')])
        elif filename.endswith('.tinydiff'):
            raw_pair = filename[0:len(filename) - len('.tinydiff')]
            pair = raw_pair.split('#')
            
            if len(pair) == 2:
                versions.append(pair[-1])
    
    return versions

if __name__ == '__main__':
    print(os.getenv("MC_VERSIONS"))
    # main()
