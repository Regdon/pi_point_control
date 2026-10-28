from collections.abc import Mapping

import static


class ConfigurationError(ValueError):
    """Raised when the application configuration is invalid."""


NODE_FIELDS = {
    "node": {"id", "type", "x", "y", "parent"},
    "node_source": {"id", "type", "x", "y", "colour"},
    "node_point_diverge": {
        "id", "type", "x", "y", "parent", "child_straight_id",
        "child_turnout_id", "point_default_state", "node", "point",
    },
    "node_point_converge": {
        "id", "type", "x", "y", "parent_straight_id",
        "parent_turnout_id", "point_default_state", "node", "point",
    },
}
POINT_TYPES = {"node_point_diverge", "node_point_converge"}
ROUTE_POINT_STATES = {
    "Straight": static.POINT_STATE_STRAIGHT,
    "Turnout": static.POINT_STATE_TURNOUT,
}


def _require_mapping(value: object, context: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ConfigurationError(f"{context} must be an object")
    return value


def _require_fields(
    value: Mapping[str, object],
    fields: set[str],
    context: str,
) -> None:
    missing = fields.difference(value)
    if missing:
        raise ConfigurationError(
            f"{context} is missing required field(s): {', '.join(sorted(missing))}"
        )


def _require_id(value: object, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConfigurationError(f"{context} must be a non-empty string")
    return value


def _require_integer(value: object, context: str) -> int:
    if isinstance(value, bool):
        raise ConfigurationError(f"{context} must be an integer")
    try:
        result = int(value)
    except (TypeError, ValueError, OverflowError) as error:
        raise ConfigurationError(f"{context} must be an integer") from error
    if isinstance(value, float) and not value.is_integer():
        raise ConfigurationError(f"{context} must be an integer")
    return result


def validate_configuration(
    node_data: object,
    route_data: object,
    toggle_data: object = None,
) -> None:
    """Validate the node, route, and optional toggle JSON documents."""
    node_document = _require_mapping(node_data, "Node configuration")
    if "nodes" not in node_document or not isinstance(node_document["nodes"], list):
        raise ConfigurationError("Node configuration must contain a 'nodes' array")

    nodes: dict[str, str] = {}
    node_records: list[tuple[str, Mapping[str, object]]] = []
    point_addresses: set[tuple[int, int]] = set()
    for index, raw_node in enumerate(node_document["nodes"]):
        context = f"Node at index {index}"
        node = _require_mapping(raw_node, context)
        node_type = node.get("type")
        if not isinstance(node_type, str) or node_type not in NODE_FIELDS:
            raise ConfigurationError(f"{context} has an unknown type: {node_type!r}")
        _require_fields(node, NODE_FIELDS[node_type], context)

        node_id = _require_id(node["id"], f"{context} id")
        if node_id in nodes:
            raise ConfigurationError(f"Duplicate node id: {node_id!r}")
        nodes[node_id] = node_type
        node_records.append((node_type, node))

        _require_integer(node["x"], f"{context} x")
        _require_integer(node["y"], f"{context} y")
        if node_type in POINT_TYPES:
            default_state = _require_integer(
                node["point_default_state"],
                f"{context} point_default_state",
            )
            if default_state not in (
                static.POINT_STATE_STRAIGHT,
                static.POINT_STATE_TURNOUT,
            ):
                raise ConfigurationError(
                    f"{context} point_default_state must be Straight or Turnout"
                )
            point_node = _require_integer(node["node"], f"{context} node")
            if not 0 <= point_node <= 3:
                raise ConfigurationError(
                    f"{context} node must be an integer between 0 and 3"
                )
            point_number = _require_integer(node["point"], f"{context} point")
            if not 0 <= point_number <= 7:
                raise ConfigurationError(
                    f"{context} point must be an integer between 0 and 7"
                )
            address = (point_node, point_number)
            if address in point_addresses:
                raise ConfigurationError(
                    f"{context} duplicates point address "
                    f"(node={point_node}, point={point_number})"
                )
            point_addresses.add(address)
        elif node_type == "node_source":
            colour = node["colour"]
            if not isinstance(colour, str) or not colour:
                raise ConfigurationError(f"{context} colour must be a non-empty string")

    for node_type, node in node_records:
        context = f"Node {node['id']!r}"
        if node_type == "node":
            _require_node_reference(node["parent"], nodes, context, "parent")
        elif node_type == "node_point_diverge":
            _require_node_reference(node["parent"], nodes, context, "parent")
            _require_node_reference(
                node["child_straight_id"], nodes, context, "child_straight_id"
            )
            _require_node_reference(
                node["child_turnout_id"], nodes, context, "child_turnout_id"
            )
        elif node_type == "node_point_converge":
            _require_node_reference(
                node["parent_straight_id"], nodes, context, "parent_straight_id"
            )
            _require_node_reference(
                node["parent_turnout_id"], nodes, context, "parent_turnout_id"
            )

    route_document = _require_mapping(route_data, "Route configuration")
    if "routes" not in route_document or not isinstance(route_document["routes"], list):
        raise ConfigurationError("Route configuration must contain a 'routes' array")

    route_ids: set[str] = set()
    for index, raw_route in enumerate(route_document["routes"]):
        context = f"Route at index {index}"
        route = _require_mapping(raw_route, context)
        _require_fields(
            route,
            {
                "id", "button_centre_x", "button_centre_y", "button_height",
                "button_width", "button_colour_scheme", "points",
            },
            context,
        )
        route_id = _require_id(route["id"], f"{context} id")
        if route_id in route_ids:
            raise ConfigurationError(f"Duplicate route id: {route_id!r}")
        route_ids.add(route_id)

        for field in ("button_centre_x", "button_centre_y"):
            _require_integer(route[field], f"{context} {field}")
        for field in ("button_height", "button_width"):
            if _require_integer(route[field], f"{context} {field}") <= 0:
                raise ConfigurationError(f"{context} {field} must be greater than zero")

        colour_scheme = route["button_colour_scheme"]
        if (
            not isinstance(colour_scheme, str)
            or colour_scheme not in static.ROUTE_COLOUR_SCHEMES
        ):
            raise ConfigurationError(f"{context} has an unknown button_colour_scheme")

        points = route["points"]
        if not isinstance(points, list):
            raise ConfigurationError(f"{context} points must be an array")
        point_ids: set[str] = set()
        for point_index, raw_point in enumerate(points):
            point_context = f"{context} point at index {point_index}"
            point = _require_mapping(raw_point, point_context)
            _require_fields(point, {"id", "state"}, point_context)
            point_id = _require_id(point["id"], f"{point_context} id")
            if point_id in point_ids:
                raise ConfigurationError(
                    f"{context} contains duplicate point id {point_id!r}"
                )
            point_ids.add(point_id)
            if nodes.get(point_id) not in POINT_TYPES:
                raise ConfigurationError(
                    f"{point_context} references unknown point node {point_id!r}"
                )
            state = point["state"]
            if not isinstance(state, str) or state not in ROUTE_POINT_STATES:
                raise ConfigurationError(
                    f"{point_context} state must be 'Straight' or 'Turnout'"
                )

    if toggle_data is None:
        return

    toggle_document = _require_mapping(toggle_data, "Toggle configuration")
    if (
        "toggles" not in toggle_document
        or not isinstance(toggle_document["toggles"], list)
    ):
        raise ConfigurationError(
            "Toggle configuration must contain a 'toggles' array"
        )

    toggle_ids: set[str] = set()
    for index, raw_toggle in enumerate(toggle_document["toggles"]):
        context = f"Toggle at index {index}"
        toggle = _require_mapping(raw_toggle, context)
        _require_fields(
            toggle,
            {
                "id", "button_centre_x", "button_centre_y", "button_height",
                "button_width", "button_colour_scheme", "default_state",
                "points", "routes", "nodes",
            },
            context,
        )
        toggle_id = _require_id(toggle["id"], f"{context} id")
        if toggle_id in toggle_ids:
            raise ConfigurationError(f"Duplicate toggle id: {toggle_id!r}")
        toggle_ids.add(toggle_id)

        for field in ("button_centre_x", "button_centre_y"):
            _require_integer(toggle[field], f"{context} {field}")
        for field in ("button_height", "button_width"):
            if _require_integer(toggle[field], f"{context} {field}") <= 0:
                raise ConfigurationError(f"{context} {field} must be greater than zero")

        colour_scheme = toggle["button_colour_scheme"]
        if (
            not isinstance(colour_scheme, str)
            or colour_scheme not in static.ROUTE_COLOUR_SCHEMES
        ):
            raise ConfigurationError(
                f"{context} has an unknown button_colour_scheme"
            )
        default_state = toggle["default_state"]
        if not isinstance(default_state, str) or default_state not in ROUTE_POINT_STATES:
            raise ConfigurationError(
                f"{context} default_state must be 'Straight' or 'Turnout'"
            )

        for field, valid_ids, description in (
            ("points", {node_id for node_id, kind in nodes.items() if kind in POINT_TYPES}, "point"),
            ("routes", route_ids, "route"),
            ("nodes", set(nodes), "node"),
        ):
            references = toggle[field]
            if not isinstance(references, list):
                raise ConfigurationError(f"{context} {field} must be an array")
            reference_ids: set[str] = set()
            for item_index, raw_reference in enumerate(references):
                reference_context = f"{context} {field[:-1]} at index {item_index}"
                reference = _require_mapping(raw_reference, reference_context)
                _require_fields(reference, {"id"}, reference_context)
                reference_id = _require_id(
                    reference["id"],
                    f"{reference_context} id",
                )
                if reference_id in reference_ids:
                    raise ConfigurationError(
                        f"{context} contains duplicate {field} id {reference_id!r}"
                    )
                reference_ids.add(reference_id)
                if reference_id not in valid_ids:
                    raise ConfigurationError(
                        f"{reference_context} references unknown {description} "
                        f"{reference_id!r}"
                    )
                if field in {"routes", "nodes"}:
                    colour = reference.get("colour")
                    if not isinstance(colour, str) or not colour:
                        raise ConfigurationError(
                            f"{reference_context} colour must be a non-empty string"
                        )


def _require_node_reference(
    value: object,
    nodes: Mapping[str, str],
    context: str,
    field: str,
) -> None:
    reference = _require_id(value, f"{context} {field}")
    if reference not in nodes:
        raise ConfigurationError(
            f"{context} {field} references unknown node {reference!r}"
        )
