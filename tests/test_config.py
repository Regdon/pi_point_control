import copy
import json
import unittest
from pathlib import Path

from data.config import ConfigurationError, validate_configuration


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIRECTORY = PROJECT_ROOT / "data"


def load_configuration():
    with (DATA_DIRECTORY / "node_data.json").open(encoding="utf-8") as file:
        node_data = json.load(file)
    with (DATA_DIRECTORY / "route_data.json").open(encoding="utf-8") as file:
        route_data = json.load(file)
    return node_data, route_data


class ConfigurationValidationTests(unittest.TestCase):
    def setUp(self):
        self.node_data, self.route_data = load_configuration()
        self.node_data = copy.deepcopy(self.node_data)
        self.route_data = copy.deepcopy(self.route_data)

    def test_repository_configuration_is_valid(self):
        validate_configuration(self.node_data, self.route_data)

    def test_rejects_unknown_node_type(self):
        self.node_data["nodes"][0]["type"] = "unknown"

        with self.assertRaisesRegex(ConfigurationError, "unknown type"):
            validate_configuration(self.node_data, self.route_data)

    def test_rejects_duplicate_node_ids(self):
        duplicate_node = copy.deepcopy(self.node_data["nodes"][0])
        self.node_data["nodes"].append(duplicate_node)

        with self.assertRaisesRegex(ConfigurationError, "Duplicate node id"):
            validate_configuration(self.node_data, self.route_data)

    def test_rejects_missing_node_reference(self):
        self.node_data["nodes"][2]["parent"] = "missing-node"

        with self.assertRaisesRegex(ConfigurationError, "unknown node"):
            validate_configuration(self.node_data, self.route_data)

    def test_rejects_invalid_default_point_state(self):
        point = next(
            node for node in self.node_data["nodes"]
            if node["type"] == "node_point_diverge"
        )
        point["point_default_state"] = "3"

        with self.assertRaisesRegex(ConfigurationError, "point_default_state"):
            validate_configuration(self.node_data, self.route_data)

    def test_rejects_missing_point_address_fields(self):
        point = next(
            node for node in self.node_data["nodes"]
            if node["type"] == "node_point_diverge"
        )
        for field in ("node", "point"):
            with self.subTest(field=field):
                value = point.pop(field)
                with self.assertRaisesRegex(
                    ConfigurationError, f"missing required field.*{field}"
                ):
                    validate_configuration(self.node_data, self.route_data)
                point[field] = value

    def test_rejects_invalid_point_address_values(self):
        point = next(
            node for node in self.node_data["nodes"]
            if node["type"] == "node_point_diverge"
        )
        for field, value, message in (
            ("node", "-1", "node must be an integer between 0 and 3"),
            ("node", "4", "node must be an integer between 0 and 3"),
            ("node", "invalid", "node must be an integer"),
            ("point", "-1", "point must be an integer between 0 and 7"),
            ("point", "8", "point must be an integer between 0 and 7"),
            ("point", "invalid", "point must be an integer"),
        ):
            with self.subTest(field=field, value=value):
                point[field] = value
                with self.assertRaisesRegex(ConfigurationError, message):
                    validate_configuration(self.node_data, self.route_data)
                point[field] = "1" if field == "node" else "0"

    def test_rejects_duplicate_point_addresses(self):
        point_nodes = [
            node for node in self.node_data["nodes"]
            if node["type"] in {"node_point_diverge", "node_point_converge"}
        ]
        point_nodes[1]["node"] = point_nodes[0]["node"]
        point_nodes[1]["point"] = point_nodes[0]["point"]

        with self.assertRaisesRegex(ConfigurationError, "duplicates point address"):
            validate_configuration(self.node_data, self.route_data)

    def test_rejects_route_reference_to_non_point_node(self):
        self.route_data["routes"][0]["points"][0]["id"] = "source_york_platform"

        with self.assertRaisesRegex(ConfigurationError, "unknown point node"):
            validate_configuration(self.node_data, self.route_data)

    def test_rejects_invalid_route_point_state(self):
        self.route_data["routes"][0]["points"][0]["state"] = "Reverse"

        with self.assertRaisesRegex(ConfigurationError, "Straight.*Turnout"):
            validate_configuration(self.node_data, self.route_data)

    def test_rejects_duplicate_route_ids(self):
        duplicate_route = copy.deepcopy(self.route_data["routes"][0])
        self.route_data["routes"].append(duplicate_route)

        with self.assertRaisesRegex(ConfigurationError, "Duplicate route id"):
            validate_configuration(self.node_data, self.route_data)


if __name__ == "__main__":
    unittest.main()
