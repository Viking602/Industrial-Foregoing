package com.buuz135.industrial.compat;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.storage.LevelResource;
import java.nio.file.Files;
import java.util.Optional;
/** Import pre-namespaced files only when the new SavedData entry does not exist. */
public final class LegacySavedData {
    public static Optional<CompoundTag> read(ServerLevel level, String name) {
        var directory = level.getServer().getWorldPath(LevelResource.ROOT).resolve("data");
        for (var file : java.util.List.of(directory.resolve(name + ".dat"), directory.resolve("minecraft").resolve(name + ".dat"))) {
            if (Files.isRegularFile(file)) {
                try {
                    var data = level.getDataStorage().readTagFromDisk(file, null, net.minecraft.SharedConstants.getCurrentVersion().dataVersion().version());
                    return Optional.of(data.getCompoundOrEmpty("data"));
                } catch (java.io.IOException e) {
                    throw new java.io.UncheckedIOException("Cannot import legacy Industrial Foregoing saved data: " + file, e);
                }
            }
        }
        return Optional.empty();
    }
}
