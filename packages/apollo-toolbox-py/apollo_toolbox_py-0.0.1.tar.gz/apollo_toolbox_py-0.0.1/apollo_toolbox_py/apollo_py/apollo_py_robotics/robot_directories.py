import json

from apollo_rust_file_pyo3 import PathBufPy
from apollo_toolbox_py.apollo_py.apollo_py_robotics.robot_preprocessed_modules.chain_module import ApolloChainModule
from apollo_toolbox_py.apollo_py.apollo_py_robotics.robot_preprocessed_modules.connections_module import ApolloConnectionsModule
from apollo_toolbox_py.apollo_py.apollo_py_robotics.robot_preprocessed_modules.dof_module import ApolloDOFModule
from apollo_toolbox_py.apollo_py.apollo_py_robotics.robot_preprocessed_modules.mesh_modules.convex_decomposition_meshes_module import \
    ApolloConvexDecompositionMeshesModule
from apollo_toolbox_py.apollo_py.apollo_py_robotics.robot_preprocessed_modules.mesh_modules.convex_hull_meshes_module import \
    ApolloConvexHullMeshesModule
from apollo_toolbox_py.apollo_py.apollo_py_robotics.robot_preprocessed_modules.mesh_modules.original_meshes_module import \
    ApolloOriginalMeshesModule
from apollo_toolbox_py.apollo_py.apollo_py_robotics.robot_preprocessed_modules.mesh_modules.plain_meshes_module import \
    ApolloPlainMeshesModule
from apollo_toolbox_py.apollo_py.apollo_py_robotics.robot_preprocessed_modules.urdf_module import ApolloURDFModule
from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_robotics.robot_runtime_modules.urdf_numpy_module import \
    ApolloURDFNumpyModule


class RobotPreprocessorRobotsDirectory:
    def __init__(self, directory: PathBufPy):
        self.directory = directory

    def get_robot_subdirectory(self, robot_name: str):
        directory = self.directory.append(robot_name)
        return RobotPreprocessorSingleRobotDirectory(robot_name, self.directory, directory)


class RobotPreprocessorSingleRobotDirectory:
    def __init__(self, robot_name: str, robots_directory: PathBufPy, directory: PathBufPy):
        self.robot_name: str = robot_name
        self.robots_directory: PathBufPy = robots_directory
        self.directory: PathBufPy = directory

    def to_urdf_module(self) -> 'ApolloURDFModule':
        dd = self.directory.append('urdf_module/module.json')
        st = dd.read_file_contents_to_string()
        d = json.loads(st)
        return ApolloURDFModule.from_dict(d)

    def to_urdf_numpy_module(self) -> 'ApolloURDFNumpyModule':
        urdf_module = self.to_urdf_module()
        return ApolloURDFNumpyModule.from_urdf_module(urdf_module)

    def to_chain_module(self) -> 'ApolloChainModule':
        dd = self.directory.append('chain_module/module.json')
        st = dd.read_file_contents_to_string()
        d = json.loads(st)
        return ApolloChainModule.from_dict(d)

    def to_dof_module(self) -> 'ApolloDOFModule':
        dd = self.directory.append('dof_module/module.json')
        st = dd.read_file_contents_to_string()
        d = json.loads(st)
        return ApolloDOFModule.from_dict(d)

    def to_connections_module(self) -> 'ApolloConnectionsModule':
        dd = self.directory.append('connections_module/module.json')
        st = dd.read_file_contents_to_string()
        d = json.loads(st)
        return ApolloConnectionsModule.from_dict(d)

    def to_original_meshes_module(self) -> 'ApolloOriginalMeshesModule':
        dd = self.directory.append('mesh_modules/original_meshes_module/module.json')
        st = dd.read_file_contents_to_string()
        d = json.loads(st)
        return ApolloOriginalMeshesModule.from_dict(d)

    def to_plain_meshes_module(self) -> 'ApolloPlainMeshesModule':
        dd = self.directory.append('mesh_modules/plain_meshes_module/module.json')
        st = dd.read_file_contents_to_string()
        d = json.loads(st)
        return ApolloPlainMeshesModule.from_dict(d)

    def to_convex_hull_meshes_module(self) -> 'ApolloConvexHullMeshesModule':
        dd = self.directory.append('mesh_modules/convex_hull_meshes_module/module.json')
        st = dd.read_file_contents_to_string()
        d = json.loads(st)
        return ApolloConvexHullMeshesModule.from_dict(d)

    def to_convex_decomposition_meshes_module(self) -> 'ApolloConvexDecompositionMeshesModule':
        dd = self.directory.append('mesh_modules/convex_decomposition_meshes_module/module.json')
        st = dd.read_file_contents_to_string()
        d = json.loads(st)
        return ApolloConvexDecompositionMeshesModule.from_dict(d)
