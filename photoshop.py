import json
from typing import Any, Callable
import shutil
import os

try:
    from gitignore import dolts_real_name
except ModuleNotFoundError:
    dolts_real_name = 'Dolt'


class RenderableBlock:
    """
            I guess I'm writing documentation now, since other people are supposed to use this.

            This class handles transporting model and texture files from a well-organized predetermined source folder,
            to a single directory which can be easily accessed by blockbench's vanilla-minded hardcodes.

            Simply create a RenderableBlock object, run RenderableBlock.write_files(), and you should be golden.
    """

    def __init__(self,
                 mod_id: str,
                 name: str,
                 abnormals_directory: str = f'/Users/{dolts_real_name}/Desktop/code',
                 naming_convention: Callable[[str], str] = lambda mod_id: mod_id.replace('_', '-'),
                 vanilla_directory: str = f'/Users/{dolts_real_name}/Desktop/code/minecraft-assets-1.20.4',
                 blockbench_directory: str = f'/Users/{dolts_real_name}/Desktop/wiki/pretend_directory',
                 custom_model_names: list[str] = None):
        """
                The constructor.

                mod_id, name: are the path, namespace of a resource location. If you want to do a
                neapolitan:adzuki_cake, mod_id would be 'neapolitan' and name would be 'adzuki_cake'.

                abnormals_directory: the folder which contains the source code of every abnormals mod.
                vanilla_directory: the folder which contains the assets of vanilla minecraft.
                naming_convention: the function that translates an abnormal mod's modid to the name you have in your folder.
                                   Defaults to replacing all underscores with hyphens, which is what IntelliJ does when
                                   cloning mods from Github.
                blockbench_directory: the folder to dump all texture and models. The folder that blockbench should import
                                      models from.
                custom_model_names: If the name of a block's models differ from that block's resource location, specify a LIST
                                    of all the models files that should automatically be transported. No path needed, only
                                    "NAME_OF_THE_FILE.json", please.
        """

        self.mod_id = mod_id
        self.name = name
        self.abnormals_directory = abnormals_directory
        self.folder_naming_convention = naming_convention
        self.folder_naming_convention = naming_convention
        self.blockbench_directory = blockbench_directory
        self.vanilla_directory = vanilla_directory
        if custom_model_names is not None:
            self.custom_model_names = custom_model_names
        else:
            self.custom_model_names = [name]

    def write_files(self):
        """
            The other function you need to run.

            Looks at the parent function of each model json.
        """
        # model is the original file
        # parent is the vanilla file
        for model, fname in self.get_paths():
            return_path = f'{self.get_return_model_path()}/{fname}'

            with open(model) as file:
                original_data: dict[str, Any] = json.load(file)
                has_parent = original_data.get('parent') is not None

                if has_parent:
                    parent_path: str = self.model_path_from_rl(original_data.get('parent'))
                    RenderableBlock.prepare_file(return_path)
                    shutil.copy(parent_path, return_path)
                else:
                    shutil.copy(model, return_path)

            with open(return_path, 'w') as return_file:
                textures: dict[str, str] = original_data.get("textures")
                # move textures to new file
                if has_parent:
                    with open(parent_path, 'r') as p:
                        parent_data = json.load(p)

                    for key, val in textures.items():
                        parent_data.get('textures')[key] = val

                for key, val in (parent_data if has_parent else original_data).get('textures').items():
                    val: str
                    key: str
                    if ':' not in val or 'minecraft:' in val:
                        return_texture_path = self.get_return_textures_path('minecraft')
                    else:
                        return_texture_path = self.get_return_textures_path(val.split(':')[0])

                    return_path = return_texture_path + '/' + self.texture_filename_from_rl(val)
                    RenderableBlock.prepare_file(return_path)
                    shutil.copy(self.texture_path_from_rl(val), return_path)

                json.dump(parent_data, return_file)

    def get_paths(self) -> list[tuple[str, str]]:
        return [((self.get_assets_path_in_mod_source() +
                  f'/models/block/{current_name}.json'), f'{current_name}.json') for current_name in
                self.custom_model_names]

    def get_assets_path_in_mod_source(self) -> str:
        return (f'{self.abnormals_directory}/'
                f'{self.folder_naming_convention(self.mod_id)}/src/main/resources/assets/{self.mod_id}')

    def get_return_model_path(self, modid=None):
        if modid is None:
            modid = self.mod_id
        return f'{self.blockbench_directory}/{modid}/models/block'

    def get_return_textures_path(self, modid=None):
        if modid is None:
            modid = self.mod_id
        return f'{self.blockbench_directory}/{modid}/textures'

    def get_vanilla_model_path(self):
        return f'{self.vanilla_directory}/assets/minecraft/models'

    def get_vanilla_texture_path(self):
        return f'{self.vanilla_directory}/assets/minecraft/textures'

    def model_path_from_rl(self, rl: str) -> str:
        if ':' not in rl or 'minecraft:' in rl:
            return self.get_vanilla_model_path() + f'/{rl}.json'
        else:
            mod_id, namespace = rl.split(':')
            return self.get_assets_path_in_mod_source() + f'/models/{namespace}.json'

    def texture_path_from_rl(self, rl: str) -> str:
        if ':' not in rl or 'minecraft:' in rl:
            return self.get_vanilla_texture_path() + f'/block/{rl}.json'
        else:
            mod_id, namespace = rl.split(':')
            return (self.get_assets_path_in_mod_source() +
                    f'/textures/{namespace}.png')

    def texture_filename_from_rl(self, rl):
        if ':' not in rl:
            return f'{rl}.png'
        else:
            mod_id, namespace = rl.split(':')
            return f'{namespace}.png'

    @staticmethod
    def prepare_file(path):
        try:
            os.makedirs(''.join([i + '/' for i in path.split('/')][:-1:]))
        except FileExistsError:
            pass
