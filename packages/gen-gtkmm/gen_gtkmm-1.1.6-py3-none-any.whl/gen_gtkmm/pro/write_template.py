# -*- coding: UTF-8 -*-

'''
Module
    write_template.py
Copyright
    Copyright (C) 2021 - 2024 Vladimir Roncevic <elektron.ronca@gmail.com>
    gen_gtkmm is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    gen_gtkmm is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Defines class WriteTemplate with attribute(s) and method(s).
    Creates an API for writing source and build modules.
'''

import sys
from typing import List, Optional
from os import getcwd, chmod, mkdir
from os.path import exists
from datetime import datetime
from string import Template

try:
    from ats_utilities.config_io.file_check import FileCheck
    from ats_utilities.console_io.verbose import verbose_message
    from ats_utilities.exceptions.ats_type_error import ATSTypeError
    from ats_utilities.exceptions.ats_value_error import ATSValueError
    from gen_gtkmm.pro.read_template import Templates
except ImportError as ats_error_message:
    # Force close python ATS ##################################################
    sys.exit(f'\n{__file__}\n{ats_error_message}\n')

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://electux.github.io/gen_gtkmm'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/electux/gen_gtkmm/blob/dev/LICENSE'
__version__ = '1.1.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WriteTemplate(FileCheck):
    '''
        Defines class WriteTemplate with attribute(s) and method(s).
        Creates an API for writing source and build modules.

        It defines:

            :attributes:
                | _GEN_VERBOSE - Console text indicator for process-phase.
            :methods:
                | __init__ - Initials WriteTemplate constructor.
                | write - Writes a templates with parameters.
    '''

    _GEN_VERBOSE: str = 'GEN_GTKMM::PRO::WRITE_TEMPLATE'

    def __init__(self, verbose: bool = False) -> None:
        '''
            Initials WriteTemplate constructor.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :exceptions: ATSTypeError
        '''
        super().__init__(verbose)
        verbose_message(verbose, [f'{self._GEN_VERBOSE.lower()} init writer'])

    def write(
        self,
        templates: Templates,
        pro_name: Optional[str],
        verbose: bool = False
    ) -> bool:
        '''
            Writes a templates with parameters.

            :param templates: List of templates
            :type templates: <Templates>
            :param pro_name: Project name | None
            :type pro_name: <Optional[str]>
            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :return: True (templates written) | False
            :rtype: <bool>
            :exceptions: ATSTypeError | ATSValueError
        '''
        error_msg: Optional[str] = None
        error_id: Optional[int] = None
        error_msg, error_id = self.check_params([
            ('list:templates', templates), ('str:pro_name', pro_name)
        ])
        if error_id == self.TYPE_ERROR:
            raise ATSTypeError(error_msg)
        if not bool(templates):
            raise ATSValueError('missing templates')
        if not bool(pro_name):
            raise ATSValueError('missing project name')
        pro_dir: str = f'{getcwd()}/{pro_name}'
        all_stat: List[bool] = []
        build_dir: str = f'{pro_dir}/build'
        model_dir: str = f'{pro_dir}/model'
        view_dir: str = f'{pro_dir}/view'
        about_dir: str = f'{view_dir}/about'
        help_dir: str = f'{view_dir}/help'
        settings_dir: str = f'{view_dir}/settings'
        num_of_modules: int = len(templates)
        module_path: Optional[str] = None
        module_content: Optional[str] = None
        if not exists(pro_dir):
            mkdir(pro_dir)
            mkdir(build_dir)
            mkdir(model_dir)
            mkdir(view_dir)
            mkdir(about_dir)
            mkdir(help_dir)
            mkdir(settings_dir)
        for pro_item in templates:
            module_name: str = list(pro_item.keys())[0]
            if any([
                'makefile'.capitalize() in module_name,
                '.mk' in module_name
            ]):
                module_path = f'{build_dir}/{module_name}'
            else:
                if 'model' in module_name:
                    module_path = f'{model_dir}/{module_name}'
                elif 'home' in module_name:
                    module_path = f'{view_dir}/{module_name}'
                elif 'about' in module_name:
                    module_path = f'{about_dir}/{module_name}'
                elif 'help' in module_name:
                    module_path = f'{help_dir}/{module_name}'
                elif 'settings' in module_name:
                    module_path = f'{settings_dir}/{module_name}'
                else:
                    module_path = f'{pro_dir}/{module_name}'
            template: Template = Template(pro_item[module_name])
            if bool(template):
                with open(module_path, 'w', encoding='utf-8') as module_file:
                    module_content = template.substitute(
                        {
                            'PRO': pro_name,
                            'DATE': f'{datetime.now()}',
                            'YEAR': f'{datetime.now().year}'
                        }
                    )
                    module_file.write(module_content)
                    chmod(module_path, 0o666)
                    self.check_path(module_path, verbose)
                    self.check_mode('w', verbose)
                    if 'makefile'.capitalize() in module_path:
                        self.check_format(
                            module_path, 'makefile', verbose
                        )
                    else:
                        self.check_format(
                            module_path, module_path.split('.')[1], verbose
                        )
                    if self.is_file_ok():
                        all_stat.append(True)
                    else:
                        all_stat.append(False)
        return all([
            bool(all_stat), all(all_stat), len(all_stat) == num_of_modules
        ])
