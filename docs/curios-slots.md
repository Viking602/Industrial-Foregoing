# Curios example slot — viking602.3

The existing `data/industrialforegoing/curios/entities/entities.json` assigned
`example` to players and armor stands alongside the ordinary Curios slots.
Curios therefore created a real slot for that name. It had no dedicated icon
or localized label, producing a missing-texture square with the tooltip
`Example`.

Release `26.1.2-3.6.39-viking602.3` removes only `example` from that assignment.
The other eleven assigned slot types, entity types, back/head slot definitions,
item tags and Curios integration code are retained. The correction is included
in this port's own data file.

The local build now uses the installed Titanium 4.0.12, JEI 29.47.0.111,
Jade 26.1.12 and FTB Library 26.1.2.9 dependencies. Four anonymous classes were
recompiled with different constant-pool ordering; their instructions and
referenced symbols are equivalent to the previous release. No gameplay source
was changed.

Verification on 2026-10-17: the Gradle build passed. In a disposable full-pack
client, the server and synchronized client had fourteen player slot types,
sixteen visible slots and no `example` slot. Armor stands retained their eleven
ordinary assigned types without `example`. A real Curios screen was opened and
captured. ProjectE's accompanying release supplies its own two corrected icons.

The first UI check used the previously installed SISE Compat, establishing that
the slot correction is supplied by Industrial Foregoing itself. The Compat
update only refreshes its existing resource guards for the new JAR filename,
after verifying that all 22 guarded source entries retain their original bytes
and SHA-256 values.

Local reports and screenshots are kept in the workspace's
`.work/verification/curios-slots-20261017` directory. Test instrumentation is not
included in either production port.
