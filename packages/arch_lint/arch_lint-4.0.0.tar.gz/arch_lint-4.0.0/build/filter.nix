let
  metadata = (builtins.fromTOML (builtins.readFile ../pyproject.toml)).project;
in
  path_filter: src:
    path_filter {
      root = src;
      include = [
        "mypy.ini"
        "pyproject.toml"
        ".pylintrc"
        (path_filter.inDirectory metadata.name)
        (path_filter.inDirectory "mock_module")
        (path_filter.inDirectory "tests")
      ];
    }
