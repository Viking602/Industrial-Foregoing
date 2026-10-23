# Industrial Foregoing / Minecraft 26.1.2 port

Local port of Industrial Foregoing 3.6.39, based on upstream commit
`ce2852db4b34af3ab1b9637cff0b327d4bb561d5` (1.21 branch).

Runtime: Minecraft 26.1.2, NeoForge 26.1.2.114, Java 25, Titanium 4.0.12.
Build version: `26.1.2-3.6.39-viking602.3`.

This release removes the stray `example` Curios slot assignment from players and
armor stands. All other slot assignments and the backpack/head-slot integrations
are retained. The correction is shipped in this port's own data, with no external
compatibility override. Local compile dependencies match the installed Titanium,
JEI, Jade and FTB Library releases.

See [slot correction and verification](docs/curios-slots.md).

The port uses the current registry IDs, component templates, recipe synchronization,
transactional transfer APIs, value-based persistence, item models, fluid models and
render-state extraction. Dedicated-server loading isolates client-only implementation
classes. Machine-owned inventories explicitly write changes back and distinguish
internal production from automation filters. Existing backpack saved-data filenames
and the previous infinity-tool fluid NBT representation have import paths.

Build from the project02 instance root:

```powershell
. .work\devtools\env.ps1
.work\Industrial-Foregoing\gradlew.bat -p .work\Industrial-Foregoing build
```

Dependencies resolve from the instance's `mods` folder; versions are specified in
`build.gradle`. Only this mod is rebuilt. Minecraft, NeoForge, LWJGL and native game
files are not patched. Runtime data and assets are shipped in the jar.

The old data-generation providers and EMI adapter are excluded from this runtime
port. The existing generated recipes, loot tables, tags and advancements are included.
JEI is the verified recipe viewer. Re-running the old migration scripts is not part
of the build; several are one-time source transformations.

In-game verification is maintained in the companion Extra Upgrades project's test
source set. See its `PORTING.md` for commands. The source and verification artifacts
are local development work, not an official upstream release.
