import os
import sys
import subprocess

MAPPINGS_DIR = 'mappings'
GRADLE_TASKS = ['clean', 'feather', 'build', 'javadoc', 'javadocJar', 'checkMappings', 'mapCalamusJar', 'mapNamedJar', 'decompileCFR', 'decompileQuiltflower', 'decompileProcyon', 'publish', 'separateMappings', 'insertMappings', 'propagateMappingsDown', 'propagateMappingsUp', 'propagateMappings']
GRADLEW = 'gradlew' if os.name == 'nt' else './gradlew'

# hack to make some versions unavailable even though mappings exist for them
UNAVAILABLE_VERSIONS = ['12w32a','12w34a','12w34b','12w36a','12w37a','12w38a','12w38b','12w39a','12w39b','12w40a','12w40b','12w41a','12w41b','12w42a','12w42b','12w49a','12w50a','12w50b','13w01a','13w01b','13w02a','13w02b','13w03a','13w04a','13w05a','13w05b','13w06a','13w07a','13w09a','13w09b','13w09c','13w10a','13w10b','13w11a']

def main():
    possible_versions = find_minecraft_versions()
    versions = []
    tasks = []
    
    args = sys.argv
    
    for i in range(1, len(args)):
        arg = args[i]
        
        if arg in possible_versions:
            if arg in UNAVAILABLE_VERSIONS:
                raise Exception('unavailable version ' + arg + '!');
            else:
                versions.append(arg)
        elif arg in GRADLE_TASKS:
            tasks.append(arg)
        else:
            raise Exception('unrecognized arg ' + arg + '!')
    
    if len(versions) == 0:
        if 'MC_VERSION' in os.environ:
            version = os.environ['MC_VERSION']
            
            if is_minecraft_version(version):
                versions.append(version)
            else:
                raise Exception('no minecraft version given!')
        else:
            versions = [version for version in possible_versions if version not in UNAVAILABLE_VERSIONS]
    if len(tasks) == 0:
        raise Exception('no gradle tasks given!')
    
    command = [GRADLEW]
    command.extend(tasks)
    command.append('--stacktrace')
    
    for version in versions:
        os.environ['MC_VERSION'] = version
        subprocess.run(" ".join(command), shell = True, check = True)

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
    main()
