from pathlib import Path
r=Path('.work/Industrial-Foregoing/src/main/java/com/buuz135/industrial')
p=r/'proxy/client/render/ContributorsCatEarsRender.java';s=p.read_text().replace('getBlockRenderer().getBlockModel(', 'getModelManager().getBlockStateModelSet().get(');p.write_text(s)
p=r/'proxy/client/render/item/MachineItemTint.java';s=p.read_text().replace('data.getString("entity")','data.getStringOr("entity", "")').replace('egg == null ? 0xFF636363 : EGG_COLORS.computeIfAbsent(egg, MachineItemTint::eggColors)[index-1]','egg.isEmpty() ? 0xFF636363 : EGG_COLORS.computeIfAbsent(egg.get().value(), MachineItemTint::eggColors)[index-1]');p.write_text(s)
p=Path('.work/Industrial-Foregoing/src/main/resources/META-INF/accesstransformer.cfg');p.write_text('# 26.1.2: public accessors and standalone model registration replace the old access transformers.\n')
p=Path('.work/IndustrialForegoingExtraUpgrades/build.gradle');s=p.read_text();s+='''
tasks.withType(JavaCompile).configureEach {
    options.fork = true
    options.forkOptions.jvmArgs += ['-Duser.language=en', '-Duser.country=US', '-Dfile.encoding=UTF-8']
}
''';p.write_text(s)
