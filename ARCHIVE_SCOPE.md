# Archive scope

## Supplied evidence

The five manuscript data files in `data/registries/` are preserved byte for byte. Their historical filenames and status fields identify the retained manuscript registries; they do not certify acceptance, complete endpoint evaluation or raw-data availability.

The 85 Table 2 rows include nine observed Utrecht conditions and additional descriptive observations. `DESCRIPTIVE` is a reporting label, not a requirement state. Each row retains its own population and stage.

The final Utrecht QA summary reports the 50-case sample, 250 scored items and aggregate outcome counts. Individual judgments, score spreadsheets, Chinese review notes, reviewer identities, adjudication reasons and evidence panels remain in the local study archive and are not redistributed. The aggregate summary is a field-selected projection of the retained final summary; author names and operational metadata are omitted.

CSV files are projections of the supplied records. List-valued cells use JSON array syntax. No numerical observations were changed. The 25 support-selection counts were transcribed from manuscript Supplement S1 and checked against its 46,502 total.

## Source identities

`metadata/evidence_sources.csv` lists the original evidence keys and SHA-256 identities from the numerical registry. These hashes identify source records; they do not imply that the source records are supplied in full. Their `original_file_included` values remain false. The aggregate QA summary is a projection of U5, not the original complete summary. Its original source hash is retained.

Evidence-key meanings:

| Key | Record |
| --- | --- |
| U1 | Frozen Utrecht scientific authority and configuration |
| U4-r3c3, U4-r4c1 | Accepted engineering pilot reports |
| U5 | Final human QA summary |
| U6 | 25-site support-selection context |
| U7 | Observed condition inventory |
| M1 | Milan diagnostic summary |
| M2 | Historical Milan claim-evidence audit |
| M3 | Final historical human QA summary |
| M4 | Historical Milan manuscript methods |

Locators such as `U4-r3c3#counts.total` are study-source references, not Internet addresses. The figure registry's `FIGSRC-*` identifiers likewise retain source hashes without providing the original files.

## Not supplied or not established

Full source datasets, complete matched-object tables, raster inputs and the original processing pipeline are not included. The verifier supplied here was prepared for this data deposit and is not that pipeline.

Three historical authority attachments remain unrecovered: the U0 pre-freeze protocol and two U2 attachments. Retained records describing their roles do not replace the missing originals.

The Utrecht results cover r3c3 and r4c1 engineering pilots. No 25-site Utrecht 800 m diagnostic provenance result, full-site matching/raster/morphology result or complete endpoint ledger is supplied. Global spatial completeness is not established. The support-selection context must not be promoted to city-wide coverage or eligibility.

Milan diagnostic, historical confirmatory, S* and QA populations are distinct. Historical morphology summaries compare within-site upper and lower roof-proxy quartiles in S*. They are not comparisons between H/L and D/N, nor Utrecht results.

Sampled visual QA is not independent surveyed-height accuracy. Passing one observed condition does not satisfy all requirements for a downstream analysis.

## Input inventory and historical identities

The raw-input inventory is a targeted inspection of the retained recovery manifest, followed by existence and size checks of the listed groups. It is not a new exhaustive disk recovery or verification against the failed original drive. The AHN manifest preserves full-file capture hashes from the retained raster-acceptance checkpoint, together with the bound original URLs and expected byte lengths. These are historical identities, not hashes recomputed from newly downloaded or recovered AHN payloads.
