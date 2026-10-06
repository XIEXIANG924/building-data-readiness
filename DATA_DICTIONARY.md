# Data dictionary

## Shared conventions

Counts are nonnegative. JSON `null` and blank CSV cells mean unavailable or inapplicable, not zero. Fractions and thresholds are on a 0–1 scale; displayed percentages multiply them by 100. JSON boolean values are true/false; existing CSV projections retain their source spellings. OSM and BAG keys are identifiers, not measurements. Import BAG keys as text to preserve leading zeros.

Terminal provenance classes are mutually exclusive: H = explicit usable height; L = height derived from usable building levels when no usable height is selected; D = default-assigned height; N = no assigned height. Raw height and levels tag/usable counts in the Milan site table are not terminal classes: both fields can exist on one object. The sum of usable-level counts is therefore not the terminal L count.

`S*` denotes the historical Milan five-site support population as defined in the manuscript, not all diagnostic sites. A QA sample is a selected subset, not the last stage of exhaustive retention.

## Numerical observations and conditions

The main registry contains `observations`, `observed_conditions`, `sources` and archive-scope metadata. Each observation uses these fields:

| Field | Meaning |
| --- | --- |
| `id` | Stable observation ID, unique within the registry |
| `label` | Measurement or reported field name |
| `population` | Objects or records to which the row applies |
| `stage` | Evaluation or processing stage |
| `unit` | Original registry unit label; see exceptions below |
| `numerator`, `denominator` | Explicit counts defining a fraction |
| `count` | Single reported quantity; may be a median rather than an integer count |
| `fraction` | Numerator divided by denominator where available |
| `condition_state` | SATISFIED, UNMET or UNKNOWN for conditions; DESCRIPTIVE for reported quantities without a gate |
| `evidence_locators` | JSON list of original study-record references |
| `rule_locator` | Original condition-definition reference, if applicable |
| `threshold` | Minimum acceptable fraction, where bound |
| `evaluation_basis` | Observed, conditional, sampled, or upper-bound basis |

For U-C01/U-C02, numerical-pass fractions are upper bounds on technical raster eligibility. An upper bound below the minimum establishes UNMET; it does not supply a final eligibility numerator. For U-C03/U-C04, plausibility is conditional on screened numerical stock. U-C05–U-C09 apply only to the fixed human QA sample.

**Unit exceptions in the preserved registry:** `roof_nodata_total` and `ground_nodata_total` count raster samples, although their original `unit` is `record`. `U-QA-scoring_items`, `U-QA-initial_concordant_items` and `U-QA-adjudicated_items` count item judgments rather than building records. Distribution-median rows store the median in `count`, with the indicated area or grid-center unit. The preserved files have not been silently edited to replace these original labels.

`endpoint_binding_complete=false`, `endpoint_action=null` and `readiness_score=null` mean that no complete endpoint evaluation or composite score is supplied by the registry.

## Milan diagnostic sites and coordinates

`milan_site_diagnostics.csv` has one row per fixed site (25 rows). `object_count` is its diagnostic OSM-object denominator. Tag-present and usable counts describe the named fields; their rates use `object_count`. `any_source_evidence_count/rate` records usable source height or levels without double counting. `legacy_assignment_complete_count/coverage` records inherited completion including defaults. `no_default_assignment_complete_count/coverage` describes completion without defaults. Empty rates at zero-object sites remain empty.

`milan_site_coordinates.csv`: `row`, `col` are lattice indices; `latitude`, `longitude` are geographic coordinates in degrees; `radius_m` is the 800 m diagnostic radius; `is_anchor` marks the lattice anchor. Latitude/longitude are not projected metre coordinates.

`milan_sstar_source_support.csv`: `HL_count` and `non_HL_count` refer to historical primary-eligible strict matched pairs within the five S* sites. Counts sum to 126 H/L and 1,553 non-H/L pairs, or 1,679 total. They do not sum to the 8,055 diagnostic objects.

## Utrecht sites and support outcomes

`utrecht_site_coordinates.csv`: `easting_m`, `northing_m` use EPSG:28992 (RD New); geographic longitude/latitude are in degrees. The diagnostic design radius is 800 m and the support radius is 1,000 m. `role` identifies the two engineering pilots. Supplied coordinates describe design, not completed diagnostic outcomes at every site.

`utrecht_support_selection.csv`: each site's `selected_osm_geometry_memberships` counts complete OSM geometries selected by intersection with its 1,000 m support disk. The retained site membership sum equals the reported distinct-object total of 46,502, but membership and distinct object counts remain different units.

`utrecht_support_outcomes.csv`: `total` is the strict-match count; `empty` is an empty roof after the 1.5 m inset; `insufficient_centers` is a nonempty inset with fewer than 140 native grid centers; `numeric_pass` is numerical success; `other` groups the remaining numerical failure categories. These four outcomes partition each pilot's strict matches. `yield_threshold` is 0.80 and `yield_state` uses the numerical upper bound.

Other rows named `overlap-*` in the numerical registry are overlapping diagnostic flags. They are not disjoint loss categories and must not be added as though they partition all matches.

## Final Utrecht QA

`utrecht_qa_summary.json` reports the fixed sample size, initial agreement count, number of adjudicated items, replacements, final case counts, thresholds, strata and site summaries. Reviewer names and individual records are not included. `source_summary_sha256` identifies the original retained summary.

`utrecht_qa_strata.csv`: `stratum` is H/L/D/N; `numerator` is final PASS cases and `denominator` is sampled cases. `pass_fraction` is their ratio and `benchmark_satisfied` refers to the 80% represented-stratum threshold. `utrecht_qa_sites.csv` supplies descriptive site PASS/sample counts; it does not introduce a site-level QA requirement.

The five scored items were correspondence, roof support, cleaned ground, seams and contamination. A case passes only when all five final item judgments pass; FAIL and unresolved UNSURE are nonpassing. The deposited summary reports outcomes and agreement accounting but does not permit reconstruction of all 250 original item judgments.

The figure registry includes a short list of manuscript visual-example identities. These selected examples are not an exhaustive QA ledger or an additional probability sample. Their visual panels are not included.

## Historical Milan morphology

`milan_morphology.csv` preserves the five site summaries. `milan_pooled_morphology.csv` preserves four pooled summaries. Values are unrounded weighted absolute standardized mean differences (SMD).

Covariates are log common-footprint area in m², common-footprint compactness, common bounding-box aspect ratio and log building count within 100 m. The comparison is between within-site upper and lower roof-proxy quartiles in S*. Overlap weights are e for the lower group and 1−e for the upper group. `propensity_in_range_fraction_T0/T1` retain the original group labels and in-range fractions; no group relabeling is introduced in this deposit.

The retained SMD limits are 0.20 within sites and 0.10 pooled. These are study thresholds, not general standards. The original weighting code, fitted models, object-level covariates and propensity values are not supplied, so these summaries are checked rather than re-estimated.

## Identities and file formats

CSV list cells are serialized JSON arrays. `metadata/file_origins.json` identifies preserved input hashes and projection methods. `metadata/evidence_sources.csv` records original source hashes and whether those original source files are included. `SHA256SUMS.txt` covers every supplied file except itself.

## Original input manifests

`raw_input_inventory.csv` counts recovered files within each stated group; it does not assert completion of all source acquisitions. `recovered_bytes` uses the retained manifest and current size checks. A zero recovered-file count does not imply that the source data never existed.

`ahn4_source_files.csv`: `product` is DSM or DTM; `tile_id` and `filename` identify the bound source file. `download_url` is the historical download location; `expected_bytes` is its original length. `historical_capture_sha256` identifies the historically captured full payload, and `header_ledger_sha256` identifies the separate original header-evidence ledger. `site_ids` lists design-site bindings with semicolon separators. Both payload flags are false because the original TIFFs were not found in the recovery manifest and are not deposited here.

`provider_licenses.csv` identifies license records, source attributions and verification status. It does not grant new rights to provider datasets.
