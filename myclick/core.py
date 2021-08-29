import os
import sys


class Command():

    def __init__(self, callback, click_params):
        self.callback = callback
        self.click_params = click_params
        help_option()(self)
        self.parse_click_params(click_params)

    def parse_click_params(self, click_params):
        """解析click装饰器收集的option,argument参数"""
        short_opts = {}  # 收集短可选参数
        long_opts = {}   # 收集长可选参数
        _args = []       # 收集位置参数名
        params = {}      # 所有参数值
        for param in click_params:
            if isinstance(param, Option):
                params[param.name] = param.value
                if param.short_opt:
                    short_opts[param.short_opt] = param
                if param.long_opt:
                    long_opts[param.long_opt] = param
            elif isinstance(param, Argument):
                _args.append(param.name)
        self.short_opts = short_opts
        self.long_opts = long_opts
        self._args = _args
        self.params = params

    def parse_cmdline_params(self, argv):
        """解析命令行参数"""
        args_list = []
        while argv:
            arg = argv.pop(0)
            if arg[:1] == '-':
                if arg[:2] == '--':
                    opt = self.long_opts[arg]
                else:
                    opt = self.short_opts[arg]
                self.params[opt.name] = True if opt.is_flag else argv.pop(0)
            else:
                args_list.append(arg)
        self.params.update(dict(zip(self._args, args_list)))

    def __call__(self):
        self.prog_name = os.path.basename(os.path.abspath(sys.argv[0]))
        self.parse_cmdline_params(sys.argv[1:])
        for param in self.click_params:
            if isinstance(param, Option) and param.is_eager \
                and self.params[param.name] and param.callback:
                param.callback(**self.params)
        temp = self.params.copy()
        if 'help' in temp: del temp['help']
        if 'version' in temp: del temp['version']
        self.callback(**temp)


    def get_help(self):
        _args = ' '.join([i.upper() for i in self._args])
        usage_help = f'Usage: {self.prog_name} [OPTIONS] {_args}'
        option_help = f'Options:\n'
        help_temp = ''
        version_temp = ''
        for param in self.click_params[::-1]:
            if isinstance(param, Option):
                temp = []
                if param.short_opt:
                    temp.append(param.short_opt)
                if param.long_opt:
                    temp.append(param.long_opt)
                temp = '  ' + ', '.join(temp)
                if param.help:
                    if len(temp) >= 20:
                        temp += '\n' + ' ' * 22 + param.help
                    else:
                        temp = f'{temp:20}  {param.help}'
                temp += '\n'
                if param.name == 'help':
                    help_temp = temp
                elif param.name == 'version':
                    version_temp = temp
                else:
                    option_help += temp
        help = usage_help + '\n\n' + option_help + version_temp + help_temp
        help = help.strip()
        return help


class Option():

    def __init__(self, param_decls=None, default=None, help=None, 
                 is_flag=False, is_eager=True, callback=None):
        self.help = help
        self.is_flag = is_flag
        self.is_eager = is_eager
        self.callback = callback
        self.parse_decls(param_decls)
        if is_flag:
            default = False
        self.value = default
    
    def parse_decls(self, param_decls):
        short_opt = None
        long_opt = None
        name = None

        for decl in param_decls:
            if decl[:2] == '--':
                long_opt = decl
            elif decl[:1] == '-':
                short_opt = decl
            else:
                name = decl
        if name is None:
            if long_opt:
                name = long_opt[2:]
            elif short_opt:
                name = short_opt[1:]
        self.short_opt = short_opt
        self.long_opt = long_opt
        self.name = name


class Argument():
    
    def __init__(self, param_decls=None):
        self.name = param_decls[0]


from .decorators import help_option
