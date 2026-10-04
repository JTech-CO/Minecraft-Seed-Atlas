# Seed provenance and version audit

## Final catalogue outcome

The final 2026-10-04 catalogue contains 400 unique seeds: 100 each for Java 26.3, 26.2, 26.1 and the 1.21 family. It adds 164 newly sourced values and retires 15 legacy values (four exact sources not recovered, eight Java 26.1 claims without sufficient evidence, one conflicting seed sign, and two similar flat island choices). The two source-supported 1.21.11 entries formerly labelled 26.1 are retained under the 1.21 family. Six inherited descriptions were narrowed to the supported terrain features.

All 400 entries have exact public source URLs. Evidence counts are 110 publisher-reported game checks, 282 publisher version listings, and eight computational map sources. There are no retained `legacy-collection` or snapshot-only entries. All 100 Java 26.3 entries use the publisher-reported release game checks. This repository did not run Minecraft to independently reproduce these worlds.

`retired_seeds.json` preserves the excluded values and reasons. The findings below describe the historical source reconstruction; unresolved historical rows are not silently treated as verified in the final catalogue.

Audit date: 2026-10-04 (Asia/Seoul). Existing atlas: 251 unique numeric seed values.

## Existing data

- Counts before update: Java 26.2 = 85, Java 26.1 = 65, 1.21 family = 101.
- All 251 numeric values fit Java's signed 64-bit integer range. No repeated seed values were found.
- Existing Markdown and generated JavaScript contain a collective bibliography rather than a source link or coordinate for each row. The `sourceLine` field identifies the local Markdown line, not a public source or verification record.
- The current builder fixes the version counts and total to 251; it validates duplicate numbers, but does not validate the signed 64-bit range, per-row provenance, coordinate limits, or source URLs. Its parser only accepts three hardcoded version labels.
- Existing assertions that every row was cross-checked cannot be reconstructed from the files. The bibliography includes mirrors and videos from the same publisher; two URLs alone do not establish independent confirmation.

## Reconstructed exact source mapping

`research-legacy-sources.json` contains 251 rows keyed by seed. 247 exact numeric seed matches were found on accessible source pages. Of these, 197 have an explicit Java source supporting the version group; 50 are listed by Cybrancee without an edition statement and remain legacy records. Four further rows remain unmapped. No local game world was generated during this audit.

| Evidence | Rows | Treatment |
|---|---:|---|
| Source explicitly lists Java and a matching version group | 197 | `source-listed`, publisher evidence |
| Exact seed in Cybrancee 26.1 article, edition unspecified | 50 | `legacy-collection`, exact link with warning |
| Exact source could not be recovered | 4 | `legacy-collection`, null URL/coordinates |

Bulk matches: [akirby80's 100 island list](https://akirby80.net/blog/top-100-minecraft-survival-island-seeds/) supplies 100 exact seeds and coordinates and explicitly says Java Edition. Four Java 26.2 collections supply 80 exact matches: [best seeds](https://akirby80.net/blog/top-10-best-minecraft-26-2-seeds-chaos-cubed-update/), [villages](https://akirby80.net/blog/top-25-village-seeds-for-minecraft-26-2/), [survival islands](https://akirby80.net/blog/top-25-survival-island-seeds-for-minecraft-26-2/), and [seeds to try](https://akirby80.net/blog/top-15-minecraft-26-2-seeds-you-need-to-try/). These are source assertions, not our in-game tests.

[Cybrancee's 50-seed article](https://cybrancee.com/blog/50-best-minecraft-seeds-for-version-26-1/) lists all 50 legacy values but does not state Java or Bedrock in the fetched content. Preserve that distinction even where the article title claims 26.1.

Coordinates in the mapping are the first documented point of interest, with its source label, and are not automatically spawn coordinates. Unknown Y values remain null. No coordinates were inferred from descriptions.

## Version corrections and source limitations

Two legacy 26.1 rows are only supported through 1.21.11 on their exact original pages and receive `recommendedVersion: "1.21"`:

- `8232298652205430997`: [WiseHosting skyscraper woodland mansion](https://wisehosting.com/minecraft-seeds/skyscraper-woodland-mansion) states Java 1.19–1.21.11.
- `416665323`: [WiseHosting infinity-loop craters](https://wisehosting.com/minecraft-seeds/infinity-loop-dual-cherry-grove-craters) states Java 1.20–1.21.11.

The akirby80 1.21 collection includes a Pale Garden seed (`147488943`) while its header generically says 1.21/Tricky Trials. The atlas should show “1.21 계열” and refrain from interpreting the collection as a guarantee for base 1.21.0. Its exact patch/snapshot is unspecified.

Four unconfirmed rows: `178707548189246514`, `1180506052330500839`, `8144877040668690370`, and `3110000067282134548`. Reddit fetches for the desert pyramid and tall ice spike were unavailable, which does not prove the links are fabricated. The [DCInside post](https://gall.dcinside.com/mgallery/board/view/?id=steve&no=331378) describes the cherry grove search but does not expose the seed number in fetched text. The [mcseedmap deep link](https://mcseedmap.net/1.21.5-Java/3110000067282134548) returns generic dynamic map text with a different sample seed; a URL containing a number is not verification of that number's features.

## Java 26.3 and 26.4

[Official Java 26.3 notes](https://www.minecraft.net/en-us/article/minecraft-java-edition-26-3) date the release to 2026-09-15 and add Dappled Forest and Abandoned Camps. A general assertion that 26.2/26.1/1.21 worlds reproduce identically in 26.3 is therefore unsupported. Require a source that actually states Java 26.3 or a separate game/generator result for every 26.3 assignment.

[Official 26.4 Snapshot 1 notes](https://www.minecraft.net/en-us/article/minecraft-26-4-snapshot-1) place the first snapshot on 2026-09-22, so it has already appeared as of the audit date. The snapshot must not be represented as a stable release seed group.

[Chunkbase Seed Map](https://www.chunkbase.com/apps/seed-map) reports an update on 2026-10-01 for MC 26.3. Its own documentation warns that coastlines are biome approximations, spawn points and several features can be inaccurate, and selected edition/version must match the generated chunks. This supports using a correctly selected 26.3 map as computational assistance, not reusing earlier labels blindly.

The [upstream Cubiomes Viewer](https://github.com/Cubitect/cubiomes-viewer) only advertises support through 1.21, and the [mja00 fork](https://github.com/mja00/cubiomes-viewer) advertises support through 26.1.2 and documents a changed 1.21.5 biome tree. Neither fetched primary document establishes Java 26.3 support. Do not generate 26.3 “verified” rows with those versions.

## Recommended canonical schema and count policy

Keep seed as a decimal string; store the supported display version group separately from a precise publisher version or range. Add `sourceName`, `sourceUrl`, `sourceVersion`, nullable `coordinates` with label and dimension, `evidenceStatus`, `evidenceNotes`, and `checkedAt`. Distinguish publisher listing, generator calculation, independently reproduced game result, and inherited legacy collection. A publisher's “tested” wording can be quoted as their claim but must not become our own game verification.

A feasible total is 301–351 by adding 50–100 sourced Java 26.3 rows while preserving the existing 251. Four groups of 100 require 400 distinct seeds: after the two version corrections, starting counts are 85/63/103, so a balanced cap of 100 per group would require 100 new 26.3, 15 new 26.2, and 37 new 26.1 seeds while choosing 100 of the 103 1.21 rows. The user's shortage allowance should be used where exact Java/version evidence is insufficient; never pad counts with invented numbers or unsupported relabeling.


## Second provenance pass (2026-10-04)

A further 36 of the 50 Cybrancee records obtained accessible matching Java 26.1 publisher evidence. The mapping now has 233 source-listed rows and 18 legacy rows, pending the collaborating researcher's additional findings. The original count table above describes the first pass and is retained as an audit trail.

- Ten rows now cite the original [akirby80 Java 26.1 collection](https://akirby80.net/blog/top-10-best-minecraft-26-1-seeds-tiny-takeover-update/) with exact seed values and XYZ points of interest.
- Three rows cite [GamesRadar's Java/Bedrock 26.1 article](https://www.gamesradar.com/best-minecraft-seeds/), which distinguishes edition-specific structures and coordinates.
- Ten rows cite [Ronimo's 26.1 collection](https://www.ronimo-games.com/best-minecraft-seeds-2026-updated-261/), explicitly labeled checked on Java 26.1. This is derivative curation with no coordinates and is lower-confidence publisher evidence, not independent discovery.
- Five feature-matching rows cite [8BitToast's 26.1 collection](https://8bittoast.com/best-minecraft-seeds/), six cite [GigaNodes' 26.1 collection](https://giganodes.host/blog/best-minecraft-seeds-26-1), and one cites [Godlike's buried mansion/outpost page](https://godlike.host/minecraft-seeds/buried-mansion-outpost/).
- One cherry/ice-spikes row cites [MC-Mod](https://www.mc-mod.net/seeds/cherry-grove-spawn-in-a-cold-mountainous-world-minecraft-seed/), which explicitly lists Java 26.1 among supported versions and credits ezseed for generator-derived coordinates. Its evidence notes retain that limitation.

PCGamesN now titles its list 26.2, so exact numeric matches there were not treated as proof of Java 26.1. TechRadar gives the positive number `8880302588844065321` for the submerged obsidian farm, while Cybrancee and 8BitToast give negative `-8880302588844065321`; the negative record remains a publisher claim with an explicit conflict note. No number or sign has been silently changed.

8BitToast gives conflicting terrain descriptions for `105849523` and `-608830374621340378`, so it was not used to upgrade those rows. Generic map version menus were not accepted as proof of the original unique terrain or geometry. No further version relocations are recommended by this pass, and no independent Minecraft world test was performed.

## Final provenance reconciliation (2026-10-04)

The second pass incorporates six additional source records from the collaborating researcher: two exact feature matches from GigaNodes, two exact Java 26.1 catalogue pages from Godlike, and two seed-specific Java 26.1 compatibility records from ezseed. This brings the 50 Cybrancee-derived rows to 42 source-listed and eight legacy-collection rows. The complete 251-row historical mapping contains 239 source-listed and 12 legacy-collection rows, including four source-null records selected for retirement. All six additions include a narrowed `recommendedDescription` that removes uncorroborated inherited details.

[Godlike's multi-village island](https://godlike.host/minecraft-seeds/multi-village-survival-island/) supports four villages in Java 26.1, but not nearby mushroom islands. [Godlike's mansion/village island](https://godlike.host/minecraft-seeds/island-with-mansion-and-village/) does not specify an exact 100-block gap. [ezseed's frozen-ocean island](https://ezseed.net/popular/seed/4251340341/) supports a village and shipwreck without establishing that the shipwreck is embedded inside the village. [ezseed's mushroom-fields catalogue](https://ezseed.net/popular/seed/4405134068028/) supports nearby mushroom fields, old-growth pine taiga and jungle; the older ice-spikes/mangrove combination is omitted. These two ezseed records distinguish the seed-specific compatibility list from the currently displayed 26.2 map data and remain publisher catalogue evidence, not our version-specific game tests.

The remaining eight Cybrancee rows retain their exact collection URLs in the historical mapping with explicit edition/version uncertainty. Shape-only matches, Java 26.2 listings, general 26.x claims and generic version menus do not verify their distinctive terrain in Java 26.1. The final-site plan retires these eight rows along with the four source-null rows and two repetitive 1.21 islands, replacing uncertain entries with explicit Java/version sources. Historical mapping counts above are therefore not final site counts.

The mapping includes Korean `evidenceNotesKo` for ten derivative Ronimo records, the conflicting obsidian-farm seed sign, and two ezseed catalogue/map-version limitations. These notes can be shown directly in the Korean interface while retaining the longer English research notes.


