
def command():
    def decorator(f):
        if hasattr(f, '__click_params__'):
            attrs = f.__click_params__
            del f.__click_params__
        else:
            attrs = []
        return Command(f, attrs)
    return decorator


def option(*param_decls, **attrs):
    def decorator(f):
        _param_memo(f, Option(param_decls, **attrs))
        return f
    return decorator


def argument(*param_decls, **attrs):
    def decorator(f):
         _param_memo(f, Argument(param_decls, **attrs))
         return f
    return decorator


def _param_memo(f, param):
    if isinstance(f, Command):
        f.click_params.append(param)
    if not hasattr(f, '__click_params__'):
         f.__click_params__ = []
    f.__click_params__.append(param)


def help_option(*param_decls, **attrs):
    def decorator(f):
        def callback(**kwargs):
            print(f.get_help())
            exit()
        attrs.update({
            'is_flag': True,
            'is_eager': True,
            'help': 'Show this message and exit.',
            'callback': callback})
        return option(*(param_decls or ('--help',)), **attrs)(f)
    return decorator


from .core import Command, Option, Argument
