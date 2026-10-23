package com.buuz135.industrial.block.core;

import com.hrznstudio.titanium.datagenerator.loot.block.BasicBlockLootTables;
import com.hrznstudio.titanium.datagenerator.loot.block.IBlockLootTableProvider;
import net.minecraft.world.level.block.SlimeBlock;
import net.minecraft.world.level.storage.loot.LootTable;

public class PinkSlimeBlock extends SlimeBlock implements IBlockLootTableProvider {

    public PinkSlimeBlock(Properties properties) {
        super(com.hrznstudio.titanium.module.DeferredRegistryHelper.applyBlockRegistrationId(properties));
    }

    @Override
    public LootTable.Builder getLootTable(BasicBlockLootTables basicBlockLootTables) {
        return basicBlockLootTables.droppingSelf(this);
    }
}
