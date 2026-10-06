"""Check deposited numerical summaries; no downloads or raw-data processing."""
from collections import Counter
import csv
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
checks = 0


def check(ok, message):
    global checks
    if not ok:
        raise ValueError(message)
    checks += 1


def close(a, b):
    return math.isclose(float(a), float(b), rel_tol=1e-10, abs_tol=1e-12)


def load(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8-sig'))


def csv_rows(name):
    with (ROOT / name).open(encoding='utf-8-sig', newline='') as h:
        return list(csv.DictReader(h))


def compare_projection(name, expected, fields=None):
    rows = csv_rows(name)
    check(len(rows) == len(expected), f'Row count: {name}')
    for got, want in zip(rows, expected):
        check(set(got) == set(fields or want), f'Columns: {name}')
        for key in got:
            value = want.get(key)
            cell = got[key]
            if value is None:
                check(cell == '', f'Null cell: {name}/{key}')
            elif isinstance(value, (dict, list)):
                check(json.loads(cell) == value, f'Array cell: {name}/{key}')
            elif isinstance(value, bool):
                check(cell.lower() == str(value).lower(), f'Boolean cell: {name}/{key}')
            elif isinstance(value, (int, float)):
                check(close(cell, value), f'Numeric cell: {name}/{key}')
            else:
                check(cell == str(value), f'Text cell: {name}/{key}')


def main():
    sums = ROOT / 'SHA256SUMS.txt'
    check(sums.exists(), 'SHA256SUMS.txt missing')
    listed = set()
    for line in sums.read_text(encoding='utf-8').splitlines():
        digest, name = line.split('  ', 1)
        p = ROOT / name
        check(p.resolve().is_relative_to(ROOT), 'Hash entry outside archive')
        check(name not in listed, 'Duplicate hash entry')
        listed.add(name)
        check(hashlib.sha256(p.read_bytes()).hexdigest() == digest, f'File identity: {name}')
    files = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()
             and p.name != 'SHA256SUMS.txt' and '__pycache__' not in p.parts
             and '.git' not in p.parts}
    check(files == listed, 'Manifest coverage differs from supplied files')

    origins = load('metadata/file_origins.json')
    for r in origins['preserved_files']:
        check(hashlib.sha256((ROOT/r['file']).read_bytes()).hexdigest() == r['source_sha256'],
              f'Preserved source: {r["file"]}')

    reg = load('data/registries/table2_numeric_registry.json')
    fig = load('data/registries/figure_data_registry_v09.json')
    plot = load('data/registries/figure5_plot_data.json')
    subset = load('data/registries/table3_observed_conditions.json')
    qa = load('data/qa/utrecht_qa_summary.json')
    obs = reg['observations']
    index = {r['id']: r for r in obs}
    check(len(index) == len(obs) == 85, 'Observation IDs/count')
    compare_projection('data/registries/table2_observations.csv', obs)
    compare_projection('data/tables/observed_conditions.csv', reg['observed_conditions'])
    check(subset['observed_conditions'] == reg['observed_conditions'], 'Condition subset mismatch')
    check(subset['source_registry_sha256'] == hashlib.sha256(
        (ROOT/'data/registries/table2_numeric_registry.json').read_bytes()).hexdigest(), 'Subset source identity')
    for r in obs:
        n, d, f, threshold = (r[k] for k in ['numerator','denominator','fraction','threshold'])
        if d is not None:
            check(d > 0 and n is not None and 0 <= n <= d, f'Counts: {r["id"]}')
            check(f is not None and close(f, n/d), f'Fraction: {r["id"]}')
        if threshold is not None:
            check(0 <= threshold <= 1, f'Threshold: {r["id"]}')
            if r['condition_state'] == 'SATISFIED':
                check(f >= threshold, f'Satisfied condition: {r["id"]}')
            elif r['condition_state'] == 'UNMET':
                check(f < threshold, f'Unmet condition: {r["id"]}')
        for locator in r['evidence_locators']:
            check(locator.split('#',1)[0] in reg['sources'], f'Evidence key: {r["id"]}')
    conditions = reg['observed_conditions']
    check(len(conditions) == 9, 'Nine observed Utrecht conditions')
    check(Counter(r['condition_state'] for r in conditions) == {'SATISFIED':7, 'UNMET':2}, 'Condition states')
    check(all(index[r['id']] == r for r in conditions), 'Conditions are not new observations')
    check(reg['endpoint_binding_complete'] is False and reg['endpoint_action'] is None
          and reg['readiness_score'] is None, 'Endpoint scope changed')

    check(fig['diagnostic_n'] == 8055 and fig['source_n'] == 1170 and fig['assigned_n'] == 4727, 'Milan diagnostic totals')
    terminal = {s: index[f'M-diagnostic-{s}']['count'] for s in 'HLDN'}
    check(terminal == dict(H=11,L=1159,D=3557,N=3328), 'Milan terminal provenance')
    check(sum(terminal.values()) == 8055, 'Milan H/L/D/N partition')
    check(terminal['H'] + terminal['L'] == 1170, 'Milan source stock')
    check(1170 + terminal['D'] == 4727, 'Milan completion stock')
    sites = fig['site_summary']
    check(len(sites) == len({r['site_id'] for r in sites}) == 25, 'Milan site count')
    check(sum(int(r['object_count']) for r in sites) == 8055, 'Site diagnostic denominator')
    check(sum(int(r['any_source_evidence_count']) for r in sites) == 1170, 'Site source count')
    check(sum(int(r['legacy_assignment_complete_count']) for r in sites) == 4727, 'Site completed count')
    high = [r['site_id'] for r in sites if int(r['object_count']) > 0
            and int(r['any_source_evidence_count']) == 0
            and float(r['legacy_assignment_coverage']) >= .9]
    check(sorted(high) == sorted(fig['zero_HL_high_completion_sites']) and len(high) == 9, 'Zero-source/high-completion sites')
    rate_map = {'height_tag_present_rate':'height_tag_present_count', 'usable_height_rate':'usable_height_count',
                'building_levels_tag_present_rate':'building_levels_tag_present_count',
                'usable_building_levels_rate':'usable_building_levels_count',
                'any_source_evidence_rate':'any_source_evidence_count',
                'legacy_assignment_coverage':'legacy_assignment_complete_count',
                'no_default_assignment_coverage':'no_default_assignment_complete_count'}
    for r in sites:
        d = int(r['object_count'])
        for rate, count in rate_map.items():
            check(r[rate] == '' if d == 0 else close(r[rate], int(r[count])/d), f'Site rate: {r["site_id"]}/{rate}')
    hl = fig['S_star_HL_by_site']
    check(sum(hl.values()) == 126 and sum(fig['S_star_non_HL_by_site'].values()) == 1553, 'Milan S* composition')
    check(sum(sorted(hl.values(), reverse=True)[:2]) == 106, 'Milan two-site concentration')
    check(index['M-M04']['numerator'] == 1767 and index['M-M04']['denominator'] == 1777, 'Milan historical yield')
    check(index['M-QA-overall']['numerator'] == 43 and index['M-QA-overall']['denominator'] == 50, 'Milan final QA')

    for row in plot['support_outcomes']:
        site = row['site_id']
        check(sum(row[k] for k in ['empty','insufficient_centers','numeric_pass','other']) == row['total'], f'Outcome partition: {site}')
        check(row['total'] == index[f'U-{site}-total']['count'], f'Strict matches: {site}')
        check(row['numeric_pass'] == index[f'U-{site}-numeric_pass']['count'], f'Numerical pass: {site}')
        check(row['empty'] == index[f'U-{site}-EMPTY_ROOF_AFTER_1_5M_INSET']['count'], f'Empty inset: {site}')
        check(row['insufficient_centers'] == index[f'U-{site}-NONEMPTY_ROOF_GRID_CENTERS_LT_140']['count'], f'Insufficient centers: {site}')
        check(row['numeric_pass']/row['total'] < row['yield_threshold'] == .8, f'Upper-bound state: {site}')
    check(sum(r['total'] for r in plot['support_outcomes']) == 3023, 'Utrecht 3023 strict matches')
    check(sum(r['numeric_pass'] for r in plot['support_outcomes']) == 463, 'Utrecht 463 numerical passes')
    check(sum(index[f'U-{s}-screened_numeric_stock']['count'] for s in ['r3c3','r4c1']) == 445, 'Utrecht screened stock')
    context = csv_rows('data/tables/utrecht_support_selection.csv')
    check(len(context) == len({r['site_id'] for r in context}) == 25, 'Support-selection sites')
    check(sum(int(r['selected_osm_geometry_memberships']) for r in context) == 46502, 'Support-selection sum')
    check(all(int(r['support_radius_m']) == 1000 for r in context), 'Support-selection radius')

    check(qa['source_summary_sha256'] == reg['sources']['U5']['original_sha256'], 'Final QA source identity')
    check(qa['frame_count'] == 445 and qa['sample_count'] == 50 and qa['scoring_items'] == 250, 'QA frame and item count')
    check(qa['initial_concordant_items'] == 244 and qa['adjudicated_items'] == 6
          and qa['initial_concordant_items'] + qa['adjudicated_items'] == 250, 'QA agreement accounting')
    check(qa['case_counts'].get('PASS',0) == 49 and qa['case_counts'].get('FAIL',0) == 1
          and qa['case_counts'].get('UNSURE',0) == 0, 'Final QA case counts')
    check(qa['pass_numerator'] == 49 and qa['pass_denominator'] == 50 and close(qa['pass_fraction'], .98), 'Final QA fraction')
    check(qa['overall_benchmark_min_pass'] == 45 and qa['replacements'] == 0, 'QA rule and replacement count')
    check(sum(r['numerator'] for r in qa['strata']) == 49 and sum(r['denominator'] for r in qa['strata']) == 50, 'QA stratum totals')
    for row in qa['strata']:
        match = next(r for r in plot['qa'] if r['stratum'] == row['stratum'])
        check(row == match, 'QA plot/summary stratum agreement')
    check(sum(r['numerator'] for r in qa['sites']) == 49 and sum(r['denominator'] for r in qa['sites']) == 50, 'QA site totals')

    compare_projection('data/tables/milan_site_diagnostics.csv', sites)
    compare_projection('data/tables/milan_site_coordinates.csv', fig['site_coordinates'])
    compare_projection('data/tables/utrecht_site_coordinates.csv', fig['Utrecht_coordinates'])
    compare_projection('data/tables/utrecht_support_outcomes.csv', plot['support_outcomes'])
    compare_projection('data/qa/utrecht_qa_strata.csv', qa['strata'])
    compare_projection('data/qa/utrecht_qa_sites.csv', qa['sites'])
    compare_projection('data/tables/milan_sstar_source_support.csv',
        [dict(site_id=s,HL_count=n,non_HL_count=fig['S_star_non_HL_by_site'][s]) for s,n in hl.items()])
    compare_projection('data/tables/milan_morphology.csv',
        [dict(site_id=r['site_id'], **r['weighted_abs_smd'],
              propensity_in_range_fraction_T0=r['propensity_in_range_fraction_T0'],
              propensity_in_range_fraction_T1=r['propensity_in_range_fraction_T1'], passed=r['passed'])
         for r in fig['morphology']['site_diagnostics']])
    compare_projection('data/tables/milan_pooled_morphology.csv',
        [dict(covariate=k,weighted_abs_smd=v) for k,v in fig['morphology']['pooled_weighted_abs_smd'].items()])
    for row in fig['morphology']['site_diagnostics']:
        check(any(x > .2 for x in row['weighted_abs_smd'].values()) and row['passed'] is False, 'Milan site SMD state')
    check(all(x <= .1 for x in fig['morphology']['pooled_weighted_abs_smd'].values())
          and fig['morphology']['pooled_passed'] is True, 'Milan pooled SMD state')
    meta = load('metadata/dataset.json')
    check(meta['reuse_license'] == 'CC-BY-4.0', 'Deposit license')
    check(meta['raw_inputs_included'] is False and meta['original_processing_code_included'] is False, 'Archive scope')
    print(f'PASS: {checks} checks; 85 observations, 9 Utrecht conditions, 25 sites per city, aggregate QA only.')
    print('Scope: supplied counts and definitions; not complete reproduction from raw inputs.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        sys.exit(1)
