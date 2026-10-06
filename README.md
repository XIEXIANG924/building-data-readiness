# Building-data readiness: numerical summaries and QA records

Supporting data for *From field completeness to analytical readiness: A provenance-aware assessment model for building data*.

This archive contains numerical summaries for two Utrecht engineering pilots and the historical western Milan case. It also supplies aggregate final Utrecht human QA counts and the 25-site Utrecht support-selection context. Individual score sheets and adjudication records are not supplied.

## Read the data

| Location | Contents |
| --- | --- |
| `data/registries/table2_numeric_registry.json` | 85 observations with populations, denominators, stages, evidence locators and condition states |
| `data/registries/table2_observations.csv` | CSV representation of the same 85 observations |
| `data/registries/table3_observed_conditions.json` | Nine observed Utrecht conditions; a subset of Table 2 |
| `data/registries/figure_data_registry_v09.json` | Retained site summaries, coordinates, Milan morphology summaries and selected QA example identities |
| `data/registries/figure5_plot_data.json` | Utrecht support-loss categories and sampled QA counts |
| `data/tables/` | Separate CSV tables for direct inspection |
| `data/qa/` | Anonymous final Utrecht QA summary, stratum counts and site counts |
| `metadata/` | File origins, source identities and dataset description |

Definitions are in [DATA_DICTIONARY.md](DATA_DICTIONARY.md); archive coverage is described in [ARCHIVE_SCOPE.md](ARCHIVE_SCOPE.md). Percentages are computed as 100 times the stored fractions. Site IDs identify positions within each city's own lattice; identical IDs across cities do not identify the same place.

## Reported summaries

| Measure | Numerator / denominator | Interpretation |
| --- | --- | --- |
| Utrecht r3c3 technical yield | 434 / 2,980 = 14.56% | Numerical-pass upper bound; below the 80% minimum |
| Utrecht r4c1 technical yield | 29 / 43 = 67.44% | Numerical-pass upper bound; below the 80% minimum |
| Utrecht sampled human QA | 49 / 50 = 98% | Final adjudicated sample; not an exhaustive eligibility stage |
| Milan source-supported fields | 1,170 / 8,055 = 14.53% | Diagnostic OSM-object population |
| Milan completed assignment | 4,727 / 8,055 = 58.68% | Diagnostic OSM-object population |
| Milan default-assigned values | 3,557 / 8,055 = 44.16% | A 44.16-percentage-point contribution to field coverage |
| Milan historical raster yield | 1,767 / 1,777 = 99.44% | Historical eligibility-based population, not Utrecht's pre-temporal construct |
| Milan sampled human QA | 43 / 50 = 86% | Final human review; two FAIL and five UNSURE |

The nine observed Utrecht conditions are not a complete endpoint ledger. The 46,502 selected OSM objects in 1,000 m support disks are not an 800 m diagnostic provenance cohort or an eligibility population.

## Verify the archive

From this directory, run:

```sh
python scripts/verify_dataset.py
```

The script uses Python 3.9 or later and the standard library. It checks file identities, JSON/CSV agreement, fractions, support-outcome partitions, final QA accounting and the principal reported counts. It performs no downloads and changes no files.

The script checks these supplied data; it does not regenerate the original OSM matching, raster measurements, temporal screening or morphology estimates.

## Coverage and reuse

Full raw inputs and the original processing code are not included. The archive supports verification of reported counts and definitions rather than complete reproduction from original inputs. Original OSM, BAG, AHN and historical Milan products remain subject to their providers' access and reuse conditions. See [RIGHTS.md](RIGHTS.md) for the current licensing status.

Files are supplied without author names, emails or local file paths. A hosting account, repository history or public metadata can still identify the depositors; file-level anonymity does not make a public repository anonymous.

## Original input inventory

`metadata/raw_input_inventory.csv` describes inputs and intermediate tables located in the recovery archive. They are not bundled here. `metadata/ahn4_source_files.csv` supplies 72 bound DSM/DTM download URLs, original expected sizes and historical capture hashes. No downloads were made in preparing this deposit. Reacquisition must check exact byte identities; a currently accessible URL alone does not prove an unchanged source version.

The AHN source TIFFs and the original global OSM history input were not located in the recovery manifest. Retained BAG pages, selected OSM geometries and Milan inputs do not remove those gaps. Provider licensing records are in `metadata/provider_licenses.csv`; their status distinguishes current official checks from retained historical evidence.
