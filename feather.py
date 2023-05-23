import os
import sys
import subprocess

MAPPINGS_DIR = 'mappings'
GRADLE_TASKS = ['clean', 'feather', 'build', 'javadoc', 'javadocJar', 'checkMappings', 'mapCalamusJar', 'mapNamedJar', 'decompileCFR', 'decompileQuiltflower', 'decompileProcyon', 'publish', 'separateMappings', 'insertMappings', 'propagateMappingsDown', 'propagateMappingsUp', 'propagateMappings']
GRADLEW = 'gradlew' if os.name == 'nt' else './gradlew'

# some jank to hide versions that are giving problems
UNAVAILABLE_VERSIONS = []
# shortcuts for versions with ugly ids
VERSION_SHORTCUTS = {
    'inf-20100630': 'inf-20100630-1835-client',
    'a1.0.5': 'a1.0.5-2149-client',
    'a1.0.13_01': 'a1.0.13_01-1444-client',
    'a1.0.14': 'a1.0.14-1659-client',
    'a1.1.0': 'a1.1.0-131933-client',
    'a1.2.3_01': 'a1.2.3_01-0958-client',
    'a0.2.5-server': 'server-a0.2.5-1004-server',
    'server-a0.2.5': 'server-a0.2.5-1004-server',
    'b1.1-client': 'b1.1-1255-client',
    'b1.1-server': 'b1.1-1245-server',
    'b1.3-client': 'b1.3-1750-client',
    'b1.3-server': 'b1.3-1731-server',
    'b1.4-client': 'b1.4-1634-client',
    'b1.4-server': 'b1.4-1507-server',
    'b1.8-pre1-server': 'b1.8-pre1-201109091357-server',
    'b1.9-pre3-client': 'b1.9-pre3-201110061402-client',
    'b1.9-pre3-server': 'b1.9-pre3-201110061350-server',
    'b1.9-pre4-client': 'b1.9-pre4-201110131434-client',
    'b1.9-pre4-server': 'b1.9-pre4-201110131440-server',
    '12w05a': '12w05a-1442',
    '12w05a-client': '12w05a-1442-client',
    '12w05a-server': '12w05a-1442-server',
    '1.0': '1.0.0',
    '1.0-client': '1.0.0-client',
    '1.0-server': '1.0.0-server',
    '1.3': '1.3-pre-07261249',
    '1.4': '1.4-pre',
    '1.4.1': '1.4.1-pre-10231538',
    '13w03a': '13w03a-1647',
    '13w05a': '13w05a-1538',
    '13w06a': '13w06a-1636',
    '13w16a': '13w16a-04192037',
    '13w16b': '13w16b-04232151',
    '13w23b': '13w23b-06080101',
    '1.6': '1.6-pre-06251516',
    '1.6.2': '1.6.2-091847',
    '1.6.3': '1.6.3-pre-171231',
    '13w36a': '13w36a-09051446',
    '13w36b': '13w36b-09061310',
    '13w41b': '13w41b-1523',
    '1.7': '1.7-pre',
    '1.7.1': '1.7.1-pre',
    '1.7.3': '1.7.3-pre',
    '1.7.7': '1.7.7-101331',
    '14w04b': '14w04b-1554',
    '14w27b': '14w27b-07021646',
    '14w34c': '14w34c-08191549',
    '16w50a': '16w50a-1438',
    '1.12-pre3': '1.12-pre3-1409',
    '2point0_red': 'af-2013-red',
    '2point0_blue': 'af-2013-blue',
    '2point0_purple': 'af-2013-purple',
    '15w14a': 'af-2015',
    '1.RV-Pre1': 'af-2016'
}

def main():
    possible_versions = find_minecraft_versions()
    versions = []
    tasks = []
    
    args = sys.argv
    
    for i in range(1, len(args)):
        arg = args[i]
        parsed_arg = parse_minecraft_version(arg, possible_versions)
        
        if parsed_arg:
            for version in parsed_arg:
                versions.append(version)
        else:
            if arg in GRADLE_TASKS:
                tasks.append(arg)
            else:
                raise Exception('unrecognized arg ' + arg + '!')
    
    if len(versions) == 0:
        if 'MC_VERSION' in os.environ:
            parsed_arg = parse_minecraft_version(os.environ['MC_VERSION'], possible_versions)
            
            if parsed_arg:
                for version in parsed_arg:
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

def parse_minecraft_version(arg, possible_versions):
    if arg in VERSION_SHORTCUTS.keys():
        return parse_minecraft_version(VERSION_SHORTCUTS[arg], possible_versions)
    versions = []
    if arg in possible_versions:
        versions.append(arg)
    else:
        client_arg = arg + '-client'
        server_arg = arg + '-server'
        if client_arg in possible_versions:
            versions.append(client_arg)
        if server_arg in possible_versions:
            versions.append(server_arg)
    for version in versions:
        if version in UNAVAILABLE_VERSIONS:
            raise Exception('version ' + version + ' is unavailable at the moment!')
    return versions

if __name__ == '__main__':
    main()
