# -*- coding: utf-8 -*-
# @Time    : 2024/7/11 12:03
# @Author  : Quanfa
# @Desc    : new version

#region import
from .path_tool import MyPath
from .project import Project
import sys



#endregion

def auto_suffix(name: str, suffix: str = None) -> str:
    if suffix == '':
        return name
    return name + '.' + suffix


class StoredDict:
    def __init__(self, save_path_parent: MyPath):
        """
        a dict that iter saved files

        Args:
            local_file (str): __file__, the path of the script.
        """
        self.save_path_parent = save_path_parent

    def __getattribute__(self, name: str):
        if not name.startswith('f_') and not name.startswith('p_'):
            return super().__getattribute__(name)

        name, suffix = super().__getattribute__(name)

        return self.save_path_parent.cat(auto_suffix(name, suffix))

    def refresh_stored_files(self):
        if not self.save_path_parent.exist():
            return

        content = f"""
from EsyPro.file_version_control import StoredDict, MyPath


class MyFiles(StoredDict):
\tdef __init__(self, save_path_parent):
\t\tsuper().__init__(save_path_parent)\n"""

        for file in self.save_path_parent.get_files(mark='', list_r=True):
            name = file.get_name()
            if name.startswith('__'):
                continue
            suffix = ''
            if '.' in name:
                name, suffix = name.split('.')

            content += f"""\t\tself.f_{name}_{suffix} = ('{name}','{suffix}')\n"""

        content += f"""\n\nfiles=MyFiles(MyPath.from_file(__file__).get_parent())\n"""

        with open(self.save_path_parent.cat('__init__.py').ensure(), 'w') as f:

            f.write(content)


class ScriptFileSaver:
    #region static properties
    _pre_launch = True

    #endregion

    def __init__(self, script_file, locals, version: int = 1):
        """
        An advisor for script assets.

        Args:
            script_file (str): __file__, the path of the script.
            locals (dict): local params, usually locals().
            version (int, optional): version, if None, point to new version. Defaults to '1'.
        """
        #region core properties
        self.locals = locals
        self.script_path = MyPath.from_file(script_file)
        self.version = version
        #endregion

        #region prelauch task
        if ScriptFileSaver._pre_launch:  # type: ignore

            sys.path.append(self.project_path)  # append project path to system 

            # append script path to system, 
            # so that the script can directly import the module in the same folder
            sys.path.append(self.script_path.get_parent())

            try:
                import torch
                def custom_repr(tensor):
                    return f'{[*tensor.size()]}-{tensor.device}:{torch._tensor_str._str(tensor)}'
                torch.Tensor.__repr__ = custom_repr  # type: ignore
            except:
                pass
            try:
                import numpy
                def custom_repr(array):
                    return f'{array.shape}:{str(array)}'
                numpy.ndarray.__repr__ = custom_repr  # type: ignore
            except:
                pass

            ScriptFileSaver._pre_launch = False  # trigger once
        #endregion

    #region properties functioned

    @property
    def save_path_parent(self):
        return self.script_path.get_parent().cat(f'_l_{self.script_name}_v{self.version}')  # save path

    @property
    def script_name(self):
        return self.script_path.get_name()[:-3]  # remove .py

    @property
    def project_path(self):
        return Project(
            MyPath(
                self.script_path.replace(
                    self.script_path.relative_to('myscripts'),
                    ''
                )
            ).get_parent()
        )

    #endregion

    def __getitem__(self, name):
        return self.path_of(name)

    def path_of(self, name: str, suffix: str = None) -> MyPath:
        """
        advice the path of the object.

        Args:
            name (str): name of the object.
            suffix (str): if None, use the type of the object.

        Returns:
            path(MyPath): the path of the object.
        """
        if suffix is None:
            suffix = str(type(self.locals[name])).split("'")[1].split('.')[-1]

        return self.save_path_parent.cat(auto_suffix(name, suffix))

    def end_script(self, show=True):
        """
        mark the end of the script.
        """
        if not self.save_path_parent.exist():
            return
        stored_files = StoredDict(self.save_path_parent)
        stored_files.refresh_stored_files()
        if show:
            print(f'All the code in {self.script_name} has been done')
