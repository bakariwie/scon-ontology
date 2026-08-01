## What this changes

## Checklist

- [ ] HermiT reports no unsatisfiable class and no inconsistency.
- [ ] `python tools/verify_release.py "scon-ontology-1.1.0.owl"` prints `PASS`.
- [ ] `python tools/verify_release.py "scon-ontology-1.1.0.owl" --signature` reports
      no missing terms.
- [ ] Every new class carries an `IAO:0000115` definition.
- [ ] `CHANGELOG.md` updated.
- [ ] No real or identifiable person data, and no credential file, is included.
