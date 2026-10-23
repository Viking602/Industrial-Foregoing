package com.buuz135.industrial.item.addon;

import com.buuz135.industrial.item.IFCustomItem;
import com.hrznstudio.titanium.block.tile.MachineTile;
import com.hrznstudio.titanium.tab.TitaniumTab;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.item.context.UseOnContext;

public abstract class AddonItem extends IFCustomItem {
    private static final ThreadLocal<net.minecraft.resources.Identifier> REGISTRATION_ID = new ThreadLocal<>();

    /** Supplies the required item ID for integrations constructing addons outside Titanium's registry. */
    public static <T extends AddonItem> T withRegistrationId(net.minecraft.resources.Identifier id, java.util.function.Supplier<T> factory) {
        var previous = REGISTRATION_ID.get();
        REGISTRATION_ID.set(id);
        try { return factory.get(); }
        finally { if (previous == null) REGISTRATION_ID.remove(); else REGISTRATION_ID.set(previous); }
    }

    private static Properties registeredProperties(Properties properties) {
        var id = REGISTRATION_ID.get();
        return id == null ? properties : properties.setId(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ITEM, id));
    }

    public AddonItem(String name, TitaniumTab tab, Properties builder) {
        super(name, tab, registeredProperties(builder));
    }

    public AddonItem(String name, TitaniumTab tab) {
        this(name, tab, new Properties());
    }

    @Override
    public InteractionResult useOn(UseOnContext context) {
        if (!context.getLevel().isClientSide()) {
            var blockpos = context.getClickedPos();
            var entity = context.getLevel().getBlockEntity(blockpos);
            if (entity instanceof MachineTile<?> machineTile) {
                var stack = context.getItemInHand().copyWithCount(1);
                if (machineTile.canAcceptAugment(stack)) {
                    var augmentInv = machineTile.getAugmentInventory();
                    for (int i = 0; i < augmentInv.getSlots(); i++) {
                        if (augmentInv.getStackInSlot(i).isEmpty()) {
                            augmentInv.setStackInSlot(i, stack);
                            context.getItemInHand().shrink(1);
                            return InteractionResult.CONSUME;
                        }
                    }
                }
            }
        }
        return super.useOn(context);
    }
}
