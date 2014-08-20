from config_manager.baseconfig import BaseConfig


class NodeController(BaseConfig):
    def __init__(self):
        super(NodeController, self).__init__(name=None,
                                             description=None,
                                             write_file_path=None,
                                             read_file_path=None,
                                             version=None)
        self.max_cores = self.create_property('max-cores')
        self.cache_size = self.create_property('cache-size')
        self.operating_system = self.create_property('operating-system')
