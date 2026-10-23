from pathlib import Path
import re, shutil

root = Path(__file__).resolve().parent
work = root.parent
for repo, version in [('Industrial-Foregoing', '3.6.39-project02.1'), ('IndustrialForegoingExtraUpgrades', '26.1.2-3.3.008-project02.1')]:
    p = work / repo
    props = (p / 'gradle.properties').read_text()
    values = {'minecraft_version':'26.1.2', 'minecraft_version_range':'[26.1.2,26.2)', 'neo_version':'26.1.2.114', 'neo_version_range':'[26.1.2.114,26.2)', 'loader_version_range':'[11,)', 'mod_version':version, 'org.gradle.jvmargs':'-Xmx4G', 'org.gradle.daemon':'true'}
    for key, value in values.items():
        props = re.sub(r'^' + re.escape(key) + r'=.*$', key + '=' + value, props, flags=re.M)
    (p/'gradle.properties').write_text(props)
    shutil.copyfile(work/'Modern-Industrialization/gradle/wrapper/gradle-wrapper.properties', p/'gradle/wrapper/gradle-wrapper.properties')
    shutil.copyfile(work/'NeoForge-MDK-reference/settings.gradle', p/'settings.gradle')
    is_if = repo == 'Industrial-Foregoing'
    deps = ['titanium-26.1.2-4.0.8.jar', 'jei-26.1.2-neoforge-29.43.0.107.jar', 'Jade-mc26.1-NeoForge-26.1.11.jar', 'patchouli-neoforge-26.1-94.jar', 'curios-neoforge-15.0.0+26.1.2.jar', 'ftb-chunks-neoforge-26.1.2.8.jar', 'ftb-library-neoforge-26.1.2.8.jar', 'ftb-teams-neoforge-26.1.2.4.jar'] if is_if else ['titanium-26.1.2-4.0.8.jar','jei-26.1.2-neoforge-29.43.0.107.jar','Jade-mc26.1-NeoForge-26.1.11.jar','kubejs-neoforge-26.1.2-8.0.6-mi26fix.jar','rhino-2101.2.8-build.91.jar']
    dependencies = '\n'.join("    implementation files('../../mods/" + f + "')" for f in deps)
    if is_if:
        dependencies += '\n    compileOnly "dev.emi:emi-neoforge:1.1.12+1.21:api"'
    else:
        dependencies += "\n    implementation files('../Industrial-Foregoing/build/libs/industrialforegoing-26.1.2-3.6.39-project02.1.jar')"
    build = '''plugins {
    id 'java-library'
    id 'net.neoforged.moddev' version '2.0.148'
}
version = VERSION_EXPR
group = mod_group_id
base { archivesName = mod_id }
java.toolchain.languageVersion = JavaLanguageVersion.of(25)
java.withSourcesJar()
repositories { maven { url = 'https://maven.terraformersmc.com/' } }
sourceSets.main.resources { srcDir 'src/generated/resources'; exclude '**/.cache/**' }
neoForge {
    version = project.neo_version
    runs {
        client { client() }
        server { server(); programArgument '--nogui' }
        gameTestServer { type = 'gameTestServer' }
    }
    mods { "${mod_id}" { sourceSet sourceSets.main } }
}
dependencies {
DEPENDENCIES
}
tasks.withType(ProcessResources).configureEach {
    def props = [minecraft_version:minecraft_version, minecraft_version_range:minecraft_version_range,
        neo_version:neo_version, neo_version_range:neo_version_range, loader_version_range:loader_version_range,
        mod_id:mod_id, mod_name:mod_name, mod_license:mod_license, mod_version:project.version,
        mod_authors:mod_authors, mod_description:mod_description]
    inputs.properties props
    filesMatching('META-INF/neoforge.mods.toml') { expand props }
}
tasks.withType(JavaCompile).configureEach {
    options.encoding = 'UTF-8'
    options.compilerArgs += ['-Xmaxerrs', '3000']
}
tasks.named('jar') { from('LICENSE') { into 'META-INF/licenses' } }
'''.replace('VERSION_EXPR', "minecraft_version + '-' + mod_version" if is_if else 'mod_version').replace('DEPENDENCIES', dependencies)
    (p/'build.gradle').write_text(build)
    for f in (p/'src').rglob('*.java'):
        text = f.read_text(encoding='utf-8')
        text = re.sub(r'\bResourceLocation\b', 'Identifier', text)
        text = text.replace('net.minecraft.Util', 'net.minecraft.util.Util')
        text = text.replace('import me.desht.pneumaticcraft.common.registry.ModFluids;\n', '')
        f.write_text(text, encoding='utf-8')
    print(repo, 'build configured')
