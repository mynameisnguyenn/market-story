"""Tests for the Learn page builders and the generated content data files."""

from src import learn


def _flow():
    return {"title": "T", "nodes": ["A", "B", "C"],
            "links": [{"source": "A", "target": "B", "value": 2},
                      {"source": "B", "target": "C", "value": 3}]}


def test_sankey_builds_and_maps_indices():
    fig = learn.sankey_figure(_flow())
    assert fig is not None and len(fig.data) == 1
    sankey = fig.data[0]
    assert list(sankey.node.label) == ["A", "B", "C"]
    assert list(sankey.link.source) == [0, 1]
    assert list(sankey.link.target) == [1, 2]


def test_sankey_none_for_empty():
    assert learn.sankey_figure(None) is None
    assert learn.sankey_figure({"nodes": [], "links": []}) is None


def test_sankey_skips_links_with_unknown_nodes():
    flow = {"nodes": ["A", "B"], "links": [{"source": "A", "target": "ZZZ", "value": 1}]}
    assert learn.sankey_figure(flow) is None  # only link is invalid -> no figure


def test_timeline_builds_and_handles_empty():
    events = [{"year": 2000, "title": "Dot-com peak", "blurb": "x", "category": "Crash"}]
    assert learn.timeline_figure(events) is not None
    assert learn.timeline_figure([]) is None


def test_loaders_return_empty_for_missing():
    assert learn.load_text("does_not_exist.md") == ""
    assert learn.load_json("does_not_exist.json") is None


def test_generated_content_files_load_and_build():
    flows = learn.load_json("flows.json")
    assert flows is not None
    for key in ("money_flow", "fed_transmission", "equity_order"):
        assert key in flows
        assert learn.sankey_figure(flows[key]) is not None   # all node refs resolve
    timeline = learn.load_json("timeline.json")
    assert learn.timeline_figure(timeline) is not None
    assert learn.load_json("players.json")
    assert learn.load_text("01_what_is_a_market.md").startswith("##")
