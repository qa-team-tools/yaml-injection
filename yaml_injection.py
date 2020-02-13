import collections
from copy import deepcopy

import requests
import yaml
from yaml.constructor import ConstructorError, SafeConstructor


class InjectionLoader(yaml.SafeLoader):
    def __init__(self, stream, auth=None):
        super().__init__(stream)
        self.data = None
        self.main_node = None
        self.auth = auth

    @classmethod
    def authorized_loader(cls, auth):
        def create_authorized_loader(stream):
            return cls(stream, auth)
        return create_authorized_loader

    def get_single_data(self):
        # Ensure that the stream contains a single document and construct it.
        node = self.get_single_node()
        self.main_node = node
        if node is not None:
            return self.construct_document(node)
        return None

    def _inject(self, mapping, value_node, source=None):
        if source:
            items = self.construct_object(value_node)
            if not isinstance(items, list):
                items = [items]
            sources = {source: items}
        else:
            sources = self.construct_mapping(value_node)
        if 'file' in sources:
            files = sources['file']
            if not isinstance(files, list):
                files = [files]
            for file in files:
                # f_name = self.construct_scalar(value_node)
                with open(file) as inn:
                    data = yaml.load(inn, self.__class__)
                mapping.update(data)
        if 'url' in sources:
            urls = sources['url']
            if not isinstance(urls, list):
                urls = [urls]
            for url in urls:
                r = requests.get(url, auth=self.auth)
                r.raise_for_status()
                data = yaml.load(r.text, self.__class__)
                mapping.update(data)
        if 'ref' in sources:
            while self.state_generators:
                state_generators = self.state_generators
                self.state_generators = []
                for generator in state_generators:
                    for dummy in generator:
                        pass

            refs = sources['ref']
            if not isinstance(refs, list):
                refs = [refs]
            for ref in refs:
                path = ref.split()
                data = self.data
                for k in path:
                    data = data[k]
                assert isinstance(data, dict)
                mapping.update(deepcopy(data))

    def construct_mapping(self, node, deep=False):
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)
        if not isinstance(node, yaml.MappingNode):
            raise ConstructorError(None, None,
                                   'expected a mapping node, but found %s' % node.id,
                                   node.start_mark)
        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, collections.abc.Hashable):
                raise ConstructorError('while constructing a mapping', node.start_mark,
                                       'found unhashable key', key_node.start_mark)
            if key_node.tag == '!inject':
                self._inject(mapping, value_node, source=key)
            elif key in mapping and isinstance(value_node, yaml.MappingNode):
                generator = self.construct_yaml_map_prepared(value_node, mapping[key])
                mapping[key] = next(generator)
                self.state_generators.append(generator)
            elif isinstance(value_node, yaml.MappingNode):
                generator = self.construct_yaml_map_implicit_preparation(value_node)
                mapping[key] = next(generator)
                self.state_generators.append(generator)
            else:
                value = self.construct_object(value_node, deep=deep)
                mapping[key] = value
        return mapping

    @staticmethod
    def update_from_prepared(data, value, prepared):
        for k, v in prepared.items():
            if k not in value:
                value[k] = prepared[k]
                continue
            if not (isinstance(value[k], dict)):
                continue
            p = deepcopy(prepared[k])
            p.update(value[k])
            value[k].update(p)
        data.update(value)

    def construct_yaml_map_prepared(self, node, prepared):
        data = {}
        yield data
        value = self.construct_mapping(node)
        self.update_from_prepared(data, value, prepared)

    def construct_yaml_map_implicit_preparation(self, node):
        data = {}
        yield data
        value = self.construct_mapping(node)
        self.update_from_prepared(data, value, data)

    def construct_object(self, node, deep=False):
        data = super().construct_object(node, deep=deep)
        if node is self.main_node:
            self.data = data
        return data


def dummy(a, b):
    pass


InjectionLoader.add_constructor('!inject', SafeConstructor.construct_yaml_str)
