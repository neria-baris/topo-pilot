# Authorship B (job 0224, test author B, black-box records side)

Read: tools/hwsg/PROTOCOL_HWSG_v1.md (via API.md/TEST_PLAN.md/CONTRACT.json), API.md, CONTRACT.json, TEST_PLAN.md; public code of reused modules (hwsc_data, hwsc_bind, hwsb_registry, hwsc_registry, hwsc_records, k4b_driver, k4b_cert) and the schema header of one hwsu obligation JSON. Never opened tools/hwsg/*.py or test_a_*.

Files: test_b_common.py (helpers, no tests), test_b_binding, test_b_streams, test_b_handoff_oracle, test_b_registry, test_b_records, test_b_train_meter, test_b_guard. Imports are lazy (mod()), so collection never needs the code.

Not covered black-box: gt.run_train with a fake launcher (needs preflight, freeze, KC_ACCEPT fixtures); go.reproduce PASS path (needs a sha-bound stage-A record); gr.build/recheck is skipped if the fixture is not constructible.

Markers (API-AMBIGUITY): audit modules= takes module objects; check_explicit fn_name is a dotted string; identity_checker reads gh.load (stubbed); source_obligation opener hook is open-like; accept-record key names for release_barrier; export_g ratio_files is a list of two paths; separation_g tables_by_world shape; window_ok/release_barrier result exposes "ok" or status PASS. OPEN-1 (streams), OPEN-2, OPEN-3 (latest obligation), OPEN-5 (mid audit), OPEN-10 (RAM) are tested as written.
