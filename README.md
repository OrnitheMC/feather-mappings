# Feather

![Build](https://img.shields.io/github/actions/workflow/status/OrnitheMC/feather-mappings/build.yml?label=Build&branch=main)
![Build All](https://img.shields.io/github/actions/workflow/status/OrnitheMC/feather-mappings/build_all.yml?label=Build%20All&branch=main)
![Publish](https://img.shields.io/github/actions/workflow/status/OrnitheMC/feather-mappings/publish.yml?label=Publish&branch=main)
![Discord](https://img.shields.io/discord/922262455453888542?color=5865F2&label=Discord&logo=Discord&logoColor=ffffff)

Feather is a set of open, unencumbered Minecraft mappings, free for everyone to use under the Creative Commons Zero license. The intention is to let 
everyone mod Minecraft freely and openly, while also being able to innovate and process the mappings as they see fit.

## Usage
To use feather-deobfuscated Minecraft for Minecraft modding or as a dependency in a Java project, you can use [loom](https://github.com/FabricMC/fabric-loom) and [ploceus](https://github.com/OrnitheMC/ploceus) Gradle plugins. See [fabric wiki tutorial](https://fabricmc.net/wiki/tutorial:setup) for more information.

To obtain a deobfuscated Minecraft jar, [`py feather.py mapMcJarsToNamed <minecraft version>`](#mapMcJarsToNamed) will generate a jar named like `<minecraft version>-feather-gen2.jar`, which can be sent to a decompiler for deobfuscated code.
You can also directly generate a mapped jar and decompile the code using one of the following commands (no need to run the `mapNamedJar` task first):
- CFR: `py feather.py decompileCFR <minecraft version>`
- Vineflower: `py feather.py decompileVineflower <minecraft version>`

## Contributing

Our goal is to provide high-quality names that make intuitive sense. In our experience, this goal is best achieved through contribution of original names, rather than copying names from other mappings projects. While we believe that discussions relating to the names used by other mappings projects can be useful, those names must stand up to scrutiny on their own - we won't accept names on the grounds that they're present in other mappings projects.

We recommend discussing your contribution with other members of the community - either directly in your pull request, or in our other community spaces. We're always happy to help if you need us

Please have a look at the [naming conventions](/CONVENTIONS.md) before submitting mappings.

### Getting Started

1. Fork and clone the repo
2. Run `py feather.py enigma <minecraft version>` to open [Enigma](https://github.com/OrnitheMC/Enigma), a user interface to easily edit the mappings
3. Save your changes in Enigma and store them by running one of the following save tasks (`py feather.py <task> <minecraft version>`):
   - `propagateMappings`: propagate your changes up and down the version graph and save them to every applicable Minecraft version (this is most likely the task you want to use)
   - `insertMappings`: save your changes only to the specified Minecraft version
   - `propagateMappingsDown`: propagate your changes down the version graph (to versions further away from the root (b1.0)) and save them to every applicable Minecraft version
   - `propagateMappingsUp`: propagate your changes up the version graph (to versions closer to the root (b1.0)) and save them to every applicable Minecraft version
4. If you wish to continue working in Enigma, make sure to reload the mappings.
5. When you're done, commit and push your work to your fork
6. Open a pull request with your changes

#### NOTE

The `enigma` task separates the mappings for the specified version out into temporary files in the `/run/` folder. Enigma will read and write to these files, and the save tasks will use these files to save the mappings back into the version graph.

- DO NOT MANUALLY EDIT THESE FILES! You may corrupt the mappings!
- Running the `enigma` task **will** overwrite these files. If you have unsaved changes, make sure to run one of the save tasks **before** running the `enigma` task to open Enigma again!
- You can safely open multiple Enigma instances for *different* Minecraft versions. You **cannot** safely open multiple Enigma instances for *one* Minecraft version.

## Gradle
Feather uses Gradle to provide a number of utility tasks for working with the mappings.

### `feather`
Download and launch the latest version of [Enigma](https://github.com/OrnitheMC/Enigma) automatically configured to use the merged jar and the mappings.

Compared to launching Enigma externally, the gradle task adds a name guesser plugin that automatically map enums and a few constant field names.

### `build`
Build a GZip'd archive containing a tiny mapping between official (obfuscated), [intermediary](https://github.com/OrnitheMC/calamus), and Feather names ("named") and packages Tiny V1 mappings into a zip archive.

### `mapMcJarsToNamed`
Builds a deobfuscated jar with Feather mappings and automapped fields (enums, etc.). Unmapped names will be filled with [intermediary](https://github.com/OrnitheMC/calamus) names.

### `decompileCFR`
Decompile the mapped source code with the CFR decompiler. **Note:** This is not designed to be recompiled.

### `decompileVineflower`
Decompile the mapped source code with the Vineflower decompiler. **Note:** This is not designed to be recompiled.

### `downloadMcJars`
Downloads the client and server Minecraft jars for the current Minecraft version to `/ornithe-cache/game-jars/` in your user gradle cache.

### `mergeJars`
Merges the client and server jars into one merged jar, located at `/ornithe-cache/game-jars/<minecraft_version>-merged.jar` in your user gradle cache.
