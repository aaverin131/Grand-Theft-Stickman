from gts.persistence.savefile import SaveFile, SaveRecord


def _make_record(timestamp: str = "2026-05-14 10:00 AM") -> SaveRecord:
    return SaveRecord(
        name="stickman.png",
        x=123,
        y=456,
        money=500,
        health=100,
        slots=["glock", "blade", "1", "1", "1", "1", "1"],
        condition="bank",
        timestamp=timestamp,
    )


def test_round_trip_single_record(tmp_path):
    sf = SaveFile(tmp_path / "saves.csv")
    record = _make_record()
    sf.append(record)
    [read_back] = sf.read_all()
    assert read_back == record


def test_append_writes_header_once(tmp_path):
    sf = SaveFile(tmp_path / "saves.csv")
    sf.append(_make_record("a"))
    sf.append(_make_record("b"))
    rows = (tmp_path / "saves.csv").read_text().strip().splitlines()
    assert rows[0].startswith("stickman,")
    assert len(rows) == 3  # header + two data rows


def test_four_slots_pads_with_none_when_empty(tmp_path):
    sf = SaveFile(tmp_path / "saves.csv")
    assert sf.four_slots() == [None, None, None, None]


def test_four_slots_pads_with_none_when_partial(tmp_path):
    sf = SaveFile(tmp_path / "saves.csv")
    a = _make_record("a")
    b = _make_record("b")
    sf.append(a)
    sf.append(b)
    assert sf.four_slots() == [a, b, None, None]


def test_four_slots_truncates_when_overfull(tmp_path):
    sf = SaveFile(tmp_path / "saves.csv")
    for i in range(6):
        sf.append(_make_record(f"t{i}"))
    slots = sf.four_slots()
    assert len(slots) == 4
    assert all(r is not None for r in slots)


def test_timestamp_preserved(tmp_path):
    sf = SaveFile(tmp_path / "saves.csv")
    sf.append(_make_record("2024-01-19 11:09 PM"))
    [r] = sf.read_all()
    assert r.timestamp == "2024-01-19 11:09 PM"


def test_read_all_handles_missing_file(tmp_path):
    sf = SaveFile(tmp_path / "missing.csv")
    assert sf.read_all() == []


def test_append_recovers_when_existing_file_lacks_trailing_newline(tmp_path):
    from gts.persistence.savefile import HEADER

    path = tmp_path / "saves.csv"
    # Write header + one row with no trailing newline — the failure mode that
    # caused the merged 27-column row in production.
    path.write_text(
        ",".join(HEADER)
        + "\nstickman.png,1,2,3,4,a,b,c,d,e,f,g,world,2024-01-01 12:00 PM"
    )
    sf = SaveFile(path)
    sf.append(_make_record("after"))
    records = sf.read_all()
    assert len(records) == 2
    assert records[1].timestamp == "after"
