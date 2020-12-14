class RangeContainers:
        def __init__(self, ContainerClass, dataset, ranges):
                self.containers = {}
                for min_range, max_range in ranges:
                        self.containers[(min_range, max_range)] = ContainerClass(dataset[min_range:max_range])
        
        def call_container(self, range, method):
                return method(self.containers[range])