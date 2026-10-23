package com.buuz135.industrial.proxy.client.render.item;

import com.buuz135.industrial.item.MobImprisonmentToolItem;
import com.buuz135.industrial.item.infinity.InfinityTier;
import com.buuz135.industrial.item.infinity.ItemInfinity;
import com.buuz135.industrial.module.ModuleTool;
import com.buuz135.industrial.utils.IFAttachments;
import com.mojang.serialization.Codec;
import com.mojang.serialization.MapCodec;
import net.minecraft.client.Minecraft;
import net.minecraft.client.color.item.ItemTintSource;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.renderer.item.ItemStackRenderState;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;
import net.minecraft.util.ARGB;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.*;
import java.util.*;

/** Item-model tint source; index corresponds to the original model's tint layer. */
public record MachineItemTint(int index) implements ItemTintSource {
    public static final MapCodec<MachineItemTint> CODEC = Codec.INT.fieldOf("index").xmap(MachineItemTint::new, MachineItemTint::index);
    private static final Map<Item, int[]> EGG_COLORS = new HashMap<>();
    public static void clearCache() { EGG_COLORS.clear(); }
    @Override public MapCodec<MachineItemTint> type() { return CODEC; }
    @Override public int calculate(ItemStack stack, ClientLevel level, LivingEntity owner) {
        if (stack.getItem() instanceof ItemInfinity && index == 0)
            return ARGB.opaque(InfinityTier.getTierBraquet(ItemInfinity.getPowerFromStack(stack)).getLeft().getTextureColor());
        if (stack.getItem() instanceof MobImprisonmentToolItem tool && index >= 1 && index <= 3) {
            var data = stack.get(IFAttachments.MOB_IMPRISONMENT_TOOL);
            if (data == null) return 0xFF636363;
            Identifier id = Identifier.tryParse(data.getStringOr("entity", ""));
            var entity = id == null ? null : BuiltInRegistries.ENTITY_TYPE.getValue(id);
            if (entity == null) return 0xFF636363;
            if (index == 3) return tool.isBlacklisted(entity) ? 0xFFDB201A : 0xFF636363;
            var egg = SpawnEggItem.byId(entity);
            return egg.isEmpty() ? 0xFF636363 : EGG_COLORS.computeIfAbsent(egg.get().value(), MachineItemTint::eggColors)[index-1];
        }
        if (index == 1) {
            var handler = com.buuz135.industrial.compat.MachineCapabilities.fluids(stack);
            if (handler != null && !handler.getFluidInTank(0).isEmpty())
                return ARGB.opaque(com.buuz135.industrial.utils.FluidUtils.getFluidColor(handler.getFluidInTank(0)));
        }
        return -1;
    }
    private static int[] eggColors(Item egg) {
        // Spawn eggs now have individual textures. Derive their two most common opaque
        // colors from the active resource pack, instead of the removed hard-coded egg palette.
        var state = new ItemStackRenderState();
        var minecraft = Minecraft.getInstance();
        minecraft.getItemModelResolver().updateForTopItem(state, new ItemStack(egg), ItemDisplayContext.NONE, minecraft.level, null, 0);
        var material = state.pickParticleMaterial(RandomSource.create(0));
        if (material == null) return new int[]{0xFF636363,0xFF636363};
        var sprite = material.sprite();
        Map<Integer,Integer> counts = new HashMap<>();
        for (int x=0;x<sprite.contents().width();x++) for (int y=0;y<sprite.contents().height();y++) {
            int color = sprite.getPixelRGBA(0,x,y);
            if (ARGB.alpha(color) > 127) counts.merge(color,1,Integer::sum);
        }
        var colors = counts.entrySet().stream().sorted(Map.Entry.<Integer,Integer>comparingByValue().reversed().thenComparingInt(Map.Entry::getKey)).map(Map.Entry::getKey).limit(2).toList();
        int first = colors.isEmpty() ? 0xFF636363 : ARGB.opaque(colors.getFirst());
        return new int[]{first, colors.size() < 2 ? first : ARGB.opaque(colors.get(1))};
    }
}
