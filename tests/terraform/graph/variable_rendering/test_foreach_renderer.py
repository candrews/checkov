import os
from unittest import mock

from checkov.terraform.graph_manager import TerraformGraphManager

TEST_DIRNAME = os.path.dirname(os.path.realpath(__file__))


@mock.patch.dict(os.environ, {"CHECKOV_ENABLE_FOREACH_HANDLING": "True"})
def test_for_each_resource():
    dir_name = 'foreach_resources/static_foreach_value'
    resources_dir = os.path.realpath(os.path.join(TEST_DIRNAME, 'resources', dir_name))

    graph_manager = TerraformGraphManager('m', ['m'])
    local_graph, tf_definitions = graph_manager.build_graph_from_source_directory(resources_dir, render_variables=True)
    assert local_graph.vertices[0].attributes.get('foreach_value') == {'bucket_a', 'bucket_b'}
    assert local_graph.vertices[1].attributes.get('foreach_value') == {'key1': '${var.a}', 'key2': '${var.b}'}
    assert not local_graph.vertices[2].attributes.get('foreach_value')
