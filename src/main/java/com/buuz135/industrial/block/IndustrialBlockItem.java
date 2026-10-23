package com.buuz135.industrial.block;

import com.hrznstudio.titanium.tab.TitaniumTab;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Block;

import javax.annotation.Nullable;

public class IndustrialBlockItem extends BlockItem{
    private TitaniumTab group;

    public IndustrialBlockItem(Block blockIn, TitaniumTab group) {
        super(blockIn, com.hrznstudio.titanium.module.DeferredRegistryHelper.applyItemRegistrationId(new Item.Properties().useBlockDescriptionPrefix()));
        this.group = group;
    }


    @Nullable
    public String getCreatorModId(ItemStack itemStack) {
        return Component.translatable("itemGroup.industrialforegoing_" + this.group.getIdentifier().getPath()).getString();
    }
    @Override
    public void appendHoverText(ItemStack stack, Item.TooltipContext context, net.minecraft.world.item.component.TooltipDisplay display, java.util.function.Consumer<Component> tooltip, net.minecraft.world.item.TooltipFlag flag) {
        super.appendHoverText(stack, context, display, tooltip, flag);
        if (getBlock() instanceof com.buuz135.industrial.block.core.FluidExtractorBlock || getBlock() instanceof com.buuz135.industrial.block.resourceproduction.WaterCondensatorBlock) {
            tooltip.accept(Component.translatable("text.industrialforegoing.tooltip.power_optional").withStyle(net.minecraft.ChatFormatting.GOLD));
        }
    }
}
