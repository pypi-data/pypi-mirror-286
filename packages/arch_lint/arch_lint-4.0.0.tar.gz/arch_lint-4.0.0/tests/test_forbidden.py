from arch_lint.forbidden import (
    check_forbidden,
)
from arch_lint.graph import (
    FullPathModule,
    ImportGraph,
)
import pytest
from typing import (
    Dict,
    FrozenSet,
)

root = "mock_module"


def _build_forbidden_allowlist(
    raw: Dict[str, FrozenSet[str]]
) -> Dict[FullPathModule, FrozenSet[FullPathModule]]:
    return {
        FullPathModule.assert_module(k): frozenset(
            FullPathModule.assert_module(i) for i in v
        )
        for k, v in raw.items()
    }


def test_forbidden() -> None:
    allowlist_map = _build_forbidden_allowlist(
        {
            "mock_module.forbidden_import.special": frozenset(
                {
                    "mock_module.forbidden_import.layer1",
                    "mock_module.forbidden_import.main",
                }
            )
        }
    )
    graph = ImportGraph.build_graph(root, True)
    check_forbidden(allowlist_map, graph)


def test_forbidden_2() -> None:
    allowlist_map = _build_forbidden_allowlist(
        {
            "mock_module.forbidden_import.special": frozenset(
                {"mock_module.forbidden_import"}
            )
        }
    )
    graph = ImportGraph.build_graph(root, True)
    check_forbidden(allowlist_map, graph)


def test_forbidden_fail() -> None:
    graph = ImportGraph.build_graph(root, True)
    with pytest.raises(Exception) as err:
        allowlist_map = _build_forbidden_allowlist(
            {
                "mock_module.forbidden_import.special": frozenset(
                    {"mock_module.forbidden_import.layer1"}
                )
            }
        )
        check_forbidden(allowlist_map, graph)
    assert (
        str(err.value)
        == "Forbidden module `mock_module.forbidden_import.special` imported by unauthorized modules i.e. frozenset({'mock_module.forbidden_import.main'})"
    )


def test_forbidden_fail_2() -> None:
    graph = ImportGraph.build_graph(root, True)
    with pytest.raises(Exception) as err:
        allowlist_map = _build_forbidden_allowlist(
            {
                "mock_module.forbidden_import.special": frozenset(
                    {"mock_module.forbidden_import.main"}
                )
            }
        )
        check_forbidden(allowlist_map, graph)
    assert (
        str(err.value)
        == "Forbidden module `mock_module.forbidden_import.special` imported by unauthorized modules i.e. frozenset({'mock_module.forbidden_import.layer1.layer2.foo'})"
    )
