import pathlib

from actusmp.codegen import convertor
from actusmp.codegen import generator
from actusmp.codegen.enums import TargetGenerator
from actusmp.codegen.enums import TargetLanguage
from actusmp.dictionary import get_dictionary
from actusmp.utils import fsys


def write(lang: TargetLanguage, dest: pathlib.Path, path_to_java_impl: pathlib.Path):
    """Writes to file system a set of code blocks to initialise an upstream library.

    :param lang: Target progamming language.
    :param dest: Path to directory to which code will be emitted.
    :param path_to_java_impl: Path to actus-code Java library from which funcs will be derived.

    """
    assert lang in TargetLanguage
    assert dest.exists and dest.is_dir
    assert path_to_java_impl.exists() and path_to_java_impl.is_dir()

    dictionary = get_dictionary()
    for typeof in TargetGenerator:
        ctx = generator.GeneratorContext(lang, typeof, dictionary, path_to_java_impl)
        for code_block, entity in generator.generate(ctx):
            code_dest = _get_path_to_code_dest(dest, ctx, entity)
            fsys.write(code_dest, code_block)


def _get_path_to_code_dest(dest: pathlib.Path, ctx: generator.GeneratorContext, entity):
    """Returns file system location to which code block will be written.

    """
    if ctx.typeof in (TargetGenerator.FuncStubPOF, TargetGenerator.FuncStubSTF):
        return _get_path_to_code_dest_2(dest, ctx, entity)
    else:
        return _get_path_to_code_dest_1(dest, ctx, entity)


def _get_path_to_code_dest_1(dest: pathlib.Path, ctx: generator.GeneratorContext, entity):
    """Returns file system location to which code block will be written.

    """
    if ctx.lang == TargetLanguage.python:
        if ctx.typeof == TargetGenerator.Enum:
            fname = f"{convertor.to_underscore_case(entity.identifier)}.py"
            return dest / "types" / "enums" / fname
        elif ctx.typeof == TargetGenerator.EnumIndex:
            return dest / "types" / "enums" / "__init__.py"
        elif ctx.typeof == TargetGenerator.FuncIndex:
            return dest / "algos" / "executor.py"
        elif ctx.typeof == TargetGenerator.FuncStubIndex:
            return dest / "algos" / f"{entity.type_info.acronym.lower()}" / "__init__.py"
        elif ctx.typeof == TargetGenerator.FuncStubDoExecuteStep:
            return dest / "algos" / f"{entity.type_info.acronym.lower()}" / "do_execute_step.py"
        elif ctx.typeof == TargetGenerator.FuncStubDoGetSchedule:
            return dest / "algos" / f"{entity.type_info.acronym.lower()}" / "do_get_schedule.py"
        elif ctx.typeof == TargetGenerator.StateSpace:
            return dest / "types" / "core" / "states.py"
        elif ctx.typeof == TargetGenerator.Termset:
            fname = f"{convertor.to_underscore_case(entity.type_info.acronym.lower())}.py"
            return dest / "types" / "terms" / fname
        elif ctx.typeof == TargetGenerator.TermsetIndex:
            return dest / "types" / "terms" / "__init__.py"

    elif ctx.lang == TargetLanguage.rust:
        if ctx.typeof == TargetGenerator.Enum:
            fname = f"{convertor.to_underscore_case(entity.identifier)}.rs"
            return dest / "types" / "enums" / fname
        elif ctx.typeof == TargetGenerator.EnumIndex:
            return dest / "types" / "enums" / "mod.rs"
        elif ctx.typeof == TargetGenerator.FuncIndex:
            return dest / "algos" / "mod.rs"
        elif ctx.typeof == TargetGenerator.FuncStubIndex:
            return dest / "algos" / f"{entity.type_info.acronym.lower()}" / "mod.rs"
        elif ctx.typeof == TargetGenerator.FuncStubDoExecuteStep:
            return dest / "algos" / f"{entity.type_info.acronym.lower()}" / "do_execute_step.rs"
        elif ctx.typeof == TargetGenerator.FuncStubDoGetSchedule:
            return dest / "algos" / f"{entity.type_info.acronym.lower()}" / "do_get_schedule.rs"
        elif ctx.typeof == TargetGenerator.StateSpace:
            return dest / "types" / "core" / "states.rs"
        elif ctx.typeof == TargetGenerator.Termset:
            fname = f"{convertor.to_underscore_case(entity.type_info.acronym.lower())}.rs"
            return dest / "types" / "terms" / fname
        elif ctx.typeof == TargetGenerator.TermsetIndex:
            return dest / "types" / "terms" / "mod.rs"

    elif ctx.lang == TargetLanguage.typescript:
        if ctx.typeof == TargetGenerator.Enum:
            return dest / "types" / "enums" / f"{convertor.to_pascal_case(entity.identifier)}.ts"
        elif ctx.typeof == TargetGenerator.EnumIndex:
            return dest / "types" / "enums" / "index.ts"
        elif ctx.typeof == TargetGenerator.FuncIndex:
            return dest / "algos" / "index.ts"
        elif ctx.typeof == TargetGenerator.FuncStubIndex:
            return dest / "algos" / f"{entity.type_info.acronym.lower()}" / "index.ts"
        elif ctx.typeof == TargetGenerator.FuncStubDoExecuteStep:
            return dest / "algos" / f"{entity.type_info.acronym.lower()}" / "doExecuteStep.ts"
        elif ctx.typeof == TargetGenerator.FuncStubDoGetSchedule:
            return dest / "algos" / f"{entity.type_info.acronym.lower()}" / "doGetSchedule.ts"
        elif ctx.typeof == TargetGenerator.StateSpace:
            return dest / "types" / "core" / "states.ts"
        elif ctx.typeof == TargetGenerator.Termset:
            fname = f"{convertor.to_pascal_case(entity.type_info.acronym.lower())}.ts"
            return dest / "types" / "terms" / fname
        elif ctx.typeof == TargetGenerator.TermsetIndex:
            return dest / "types" / "terms" / "index.ts"


def _get_path_to_code_dest_2(dest: pathlib.Path, ctx: generator.GeneratorContext, entity):
    """Returns file system location to which code block will be written.

    """
    (defn, f_type, event_type, suffix) = entity

    fname = f"{f_type.name.lower()}_{event_type}"
    fname = f"{fname}_{suffix}" if suffix else f"{fname}"

    if ctx.lang == TargetLanguage.python:
        outdir = dest / "algos" / f"{defn.type_info.acronym.lower()}"
    elif ctx.lang == TargetLanguage.rust:
        outdir = dest / "algos" / f"{defn.type_info.acronym.lower()}"
    elif ctx.lang == TargetLanguage.typescript:
        outdir = dest / "algos" / f"{defn.type_info.acronym.lower()}"

    if ctx.lang == TargetLanguage.python:
        return outdir / f"{fname.lower()}.py"
    elif ctx.lang == TargetLanguage.rust:
        return outdir / f"{fname.lower()}.rs"
    elif ctx.lang == TargetLanguage.typescript:
        return outdir / f"{fname}.ts"
