import asyncio
import multiprocessing
import shutil
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import (
    Optional,
    Union,
    overload,
)

if sys.version_info >= (3, 9):
    from collections.abc import (
        AsyncGenerator,
        Callable,
        Collection,
        Iterator,
        Sequence,
        Set,
    )
else:
    from typing import AbstractSet as Set
    from typing import AsyncGenerator, Callable, Collection, Iterator, Sequence

import aioshutil

from ._files import FoamFieldFile, FoamFile
from ._util import is_sequence, run_process, run_process_async


class FoamCaseBase(Sequence["FoamCaseBase.TimeDirectory"]):
    def __init__(self, path: Union[Path, str] = Path()):
        self.path = Path(path).absolute()

    class TimeDirectory(Set[FoamFieldFile]):
        """
        An OpenFOAM time directory in a case.

        Use to access field files in the directory, e.g. `time["U"]`.

        :param path: The path to the time directory.
        """

        def __init__(self, path: Union[Path, str]):
            self.path = Path(path).absolute()

        @property
        def time(self) -> float:
            """The time that corresponds to this directory."""
            return float(self.path.name)

        @property
        def name(self) -> str:
            """The name of this time directory."""
            return self.path.name

        def __getitem__(self, key: str) -> FoamFieldFile:
            if (self.path / key).is_file():
                return FoamFieldFile(self.path / key)
            elif (self.path / f"{key}.gz").is_file():
                return FoamFieldFile(self.path / f"{key}.gz")
            else:
                raise KeyError(key)

        def __contains__(self, obj: object) -> bool:
            if isinstance(obj, FoamFieldFile):
                return obj.path.parent == self.path
            elif isinstance(obj, str):
                return (self.path / obj).is_file() or (
                    self.path / f"{obj}.gz"
                ).is_file()
            else:
                return False

        def __iter__(self) -> Iterator[FoamFieldFile]:
            for p in self.path.iterdir():
                if p.is_file() and (
                    p.suffix != ".gz" or not p.with_suffix("").is_file()
                ):
                    yield FoamFieldFile(p)

        def __len__(self) -> int:
            return len(list(iter(self)))

        def __fspath__(self) -> str:
            return str(self.path)

        def __repr__(self) -> str:
            return f"{type(self).__qualname__}('{self.path}')"

        def __str__(self) -> str:
            return str(self.path)

    @property
    def _times(self) -> Sequence["FoamCaseBase.TimeDirectory"]:
        times = []
        for p in self.path.iterdir():
            if p.is_dir():
                try:
                    float(p.name)
                except ValueError:
                    pass
                else:
                    times.append(FoamCaseBase.TimeDirectory(p))

        times.sort(key=lambda t: t.time)

        return times

    @overload
    def __getitem__(
        self, index: Union[int, float, str]
    ) -> "FoamCaseBase.TimeDirectory": ...

    @overload
    def __getitem__(self, index: slice) -> Sequence["FoamCaseBase.TimeDirectory"]: ...

    def __getitem__(
        self, index: Union[int, slice, float, str]
    ) -> Union["FoamCaseBase.TimeDirectory", Sequence["FoamCaseBase.TimeDirectory"]]:
        if isinstance(index, str):
            return FoamCaseBase.TimeDirectory(self.path / index)
        elif isinstance(index, float):
            for time in self._times:
                if time.time == index:
                    return time
            raise IndexError(f"Time {index} not found")
        return self._times[index]

    def __len__(self) -> int:
        return len(self._times)

    def _clean_paths(self) -> Set[Path]:
        has_decompose_par_dict = (self.path / "system" / "decomposeParDict").is_file()
        has_block_mesh_dict = (self.path / "system" / "blockMeshDict").is_file()

        paths = set()

        for p in self.path.iterdir():
            if p.is_dir():
                try:
                    t = float(p.name)
                except ValueError:
                    pass
                else:
                    if t != 0:
                        paths.add(p)

                if has_decompose_par_dict and p.name.startswith("processor"):
                    paths.add(p)

        if (self.path / "0.orig").is_dir() and (self.path / "0").is_dir():
            paths.add(self.path / "0")

        if has_block_mesh_dict and (self.path / "constant" / "polyMesh").exists():
            paths.add(self.path / "constant" / "polyMesh")

        if self._run_script() is not None:
            paths.update(self.path.glob("log.*"))

        return paths

    def _clone_ignore(
        self,
    ) -> Callable[[Union[Path, str], Collection[str]], Collection[str]]:
        clean_paths = self._clean_paths()

        def ignore(path: Union[Path, str], names: Collection[str]) -> Collection[str]:
            paths = {Path(path) / name for name in names}
            return {p.name for p in paths.intersection(clean_paths)}

        return ignore

    def _clean_script(self) -> Optional[Path]:
        """Return the path to the (All)clean script, or None if no clean script is found."""
        clean = self.path / "clean"
        all_clean = self.path / "Allclean"

        if clean.is_file():
            return clean
        elif all_clean.is_file():
            return all_clean
        else:
            return None

    def _run_script(self, *, parallel: Optional[bool] = None) -> Optional[Path]:
        """Return the path to the (All)run script, or None if no run script is found."""
        run = self.path / "run"
        run_parallel = self.path / "run-parallel"
        all_run = self.path / "Allrun"
        all_run_parallel = self.path / "Allrun-parallel"

        if run.is_file() or all_run.is_file():
            if run_parallel.is_file() or all_run_parallel.is_file():
                if parallel:
                    return run_parallel if run_parallel.is_file() else all_run_parallel
                elif parallel is False:
                    return run if run.is_file() else all_run
                else:
                    raise ValueError(
                        "Both (All)run and (All)run-parallel scripts are present. Please specify parallel argument."
                    )
            return run if run.is_file() else all_run
        elif parallel is not False and (
            run_parallel.is_file() or all_run_parallel.is_file()
        ):
            return run_parallel if run_parallel.is_file() else all_run_parallel
        else:
            return None

    def _parallel_cmd(
        self, cmd: Union[Sequence[Union[str, Path]], str, Path]
    ) -> Union[Sequence[Union[str, Path]], str]:
        if not is_sequence(cmd):
            return f"mpiexec -np {self._nprocessors} {cmd} -parallel"
        else:
            return [
                "mpiexec",
                "-np",
                str(self._nprocessors),
                cmd[0],
                "-parallel",
                *cmd[1:],
            ]

    @property
    def name(self) -> str:
        """The name of the case."""
        return self.path.name

    def file(self, path: Union[Path, str]) -> FoamFile:
        """Return a FoamFile object for the given path in the case."""
        return FoamFile(self.path / path)

    @property
    def _nsubdomains(self) -> Optional[int]:
        """Return the number of subdomains as set in the decomposeParDict, or None if no decomposeParDict is found."""
        try:
            nsubdomains = self.decompose_par_dict["numberOfSubdomains"]
            if not isinstance(nsubdomains, int):
                raise TypeError(
                    f"numberOfSubdomains in {self.decompose_par_dict} is not an integer"
                )
            return nsubdomains
        except FileNotFoundError:
            return None

    @property
    def _nprocessors(self) -> int:
        """Return the number of processor directories in the case."""
        return len(list(self.path.glob("processor*")))

    @property
    def application(self) -> str:
        """The application name as set in the controlDict."""
        application = self.control_dict["application"]
        if not isinstance(application, str):
            raise TypeError(f"application in {self.control_dict} is not a string")
        return application

    @property
    def control_dict(self) -> FoamFile:
        """The controlDict file."""
        return self.file("system/controlDict")

    @property
    def fv_schemes(self) -> FoamFile:
        """The fvSchemes file."""
        return self.file("system/fvSchemes")

    @property
    def fv_solution(self) -> FoamFile:
        """The fvSolution file."""
        return self.file("system/fvSolution")

    @property
    def decompose_par_dict(self) -> FoamFile:
        """The decomposeParDict file."""
        return self.file("system/decomposeParDict")

    @property
    def block_mesh_dict(self) -> FoamFile:
        """The blockMeshDict file."""
        return self.file("system/blockMeshDict")

    @property
    def transport_properties(self) -> FoamFile:
        """The transportProperties file."""
        return self.file("constant/transportProperties")

    @property
    def turbulence_properties(self) -> FoamFile:
        """The turbulenceProperties file."""
        return self.file("constant/turbulenceProperties")

    def __fspath__(self) -> str:
        return str(self.path)

    def __repr__(self) -> str:
        return f"{type(self).__qualname__}('{self.path}')"

    def __str__(self) -> str:
        return str(self.path)


class FoamCase(FoamCaseBase):
    """
    An OpenFOAM case.

    Provides methods for running and cleaning cases, as well as accessing files.

    Access the time directories of the case as a sequence, e.g. `case[0]` or `case[-1]`.

    :param path: The path to the case directory.
    """

    def clean(
        self,
        *,
        script: bool = True,
        check: bool = False,
    ) -> None:
        """
        Clean this case.

        :param script: If True, use an (All)clean script if it exists. If False, ignore any clean scripts.
        :param check: If True, raise a CalledProcessError if the clean script returns a non-zero exit code.
        """
        script_path = self._clean_script() if script else None

        if script_path is not None:
            self.run([script_path], check=check)
        else:
            for p in self._clean_paths():
                if p.is_dir():
                    shutil.rmtree(p)
                else:
                    p.unlink()

    def run(
        self,
        cmd: Optional[Union[Sequence[Union[str, Path]], str, Path]] = None,
        *,
        script: bool = True,
        parallel: Optional[bool] = None,
        check: bool = True,
    ) -> None:
        """
        Run this case, or a specified command in the context of this case.

        :param cmd: The command to run. If None, run the case. If a sequence, the first element is the command and the rest are arguments. If a string, `cmd` is executed in a shell.
        :param script: If True and `cmd` is None, use an (All)run(-parallel) script if it exists for running the case. If False or no run script is found, autodetermine the command(s) needed to run the case.
        :param parallel: If True, run in parallel using MPI. If None, autodetect whether to run in parallel.
        :param check: If True, raise a CalledProcessError if any command returns a non-zero exit code.
        """
        if cmd is not None:
            if parallel:
                cmd = self._parallel_cmd(cmd)

            run_process(
                cmd,
                check=check,
                cwd=self.path,
            )
        else:
            script_path = self._run_script(parallel=parallel) if script else None

            if script_path is not None:
                return self.run([script_path], check=check)

            else:
                if not self and (self.path / "0.orig").is_dir():
                    self.restore_0_dir()

                if (self.path / "system" / "blockMeshDict").is_file():
                    self.block_mesh()

                if parallel is None:
                    parallel = (
                        self._nprocessors > 0
                        or (self.path / "system" / "decomposeParDict").is_file()
                    )

                if parallel:
                    if (
                        self._nprocessors == 0
                        and (self.path / "system" / "decomposeParDict").is_file()
                    ):
                        self.decompose_par()

                self.run(
                    [self.application],
                    parallel=parallel,
                    check=check,
                )

    def block_mesh(self, *, check: bool = True) -> None:
        """Run blockMesh on this case."""
        self.run(["blockMesh"], check=check)

    def decompose_par(self, *, check: bool = True) -> None:
        """Decompose this case for parallel running."""
        self.run(["decomposePar"], check=check)

    def reconstruct_par(self, *, check: bool = True) -> None:
        """Reconstruct this case after parallel running."""
        self.run(["reconstructPar"], check=check)

    def restore_0_dir(self) -> None:
        """Restore the 0 directory from the 0.orig directory."""
        shutil.rmtree(self.path / "0", ignore_errors=True)
        shutil.copytree(self.path / "0.orig", self.path / "0")

    def copy(self, dest: Union[Path, str]) -> "FoamCase":
        """
        Make a copy of this case.

        :param dest: The destination path.
        """
        return FoamCase(shutil.copytree(self.path, dest, symlinks=True))

    def clone(self, dest: Union[Path, str]) -> "FoamCase":
        """
        Clone this case (make a clean copy).

        :param dest: The destination path.
        """
        if self._clean_script() is not None:
            copy = self.copy(dest)
            copy.clean()
            return copy

        dest = Path(dest)

        shutil.copytree(self.path, dest, symlinks=True, ignore=self._clone_ignore())

        return FoamCase(dest)


class AsyncFoamCase(FoamCaseBase):
    """
    An OpenFOAM case with asynchronous support.

    Provides methods for running and cleaning cases, as well as accessing files.

    Access the time directories of the case as a sequence, e.g. `case[0]` or `case[-1]`.

    :param path: The path to the case directory.
    """

    max_cpus = multiprocessing.cpu_count()
    """
    Maximum number of CPUs to use for running `AsyncFoamCase`s concurrently. Defaults to the number of CPUs on the system.
    """

    _reserved_cpus = 0
    _cpus_cond = None  # Cannot be initialized here yet

    @staticmethod
    @asynccontextmanager
    async def _cpus(cpus: int) -> AsyncGenerator[None, None]:
        if AsyncFoamCase._cpus_cond is None:
            AsyncFoamCase._cpus_cond = asyncio.Condition()

        cpus = min(cpus, AsyncFoamCase.max_cpus)
        if cpus > 0:
            async with AsyncFoamCase._cpus_cond:
                await AsyncFoamCase._cpus_cond.wait_for(
                    lambda: AsyncFoamCase.max_cpus - AsyncFoamCase._reserved_cpus
                    >= cpus
                )
                AsyncFoamCase._reserved_cpus += cpus
        try:
            yield
        finally:
            if cpus > 0:
                async with AsyncFoamCase._cpus_cond:
                    AsyncFoamCase._reserved_cpus -= cpus
                    AsyncFoamCase._cpus_cond.notify(cpus)

    async def clean(
        self,
        *,
        script: bool = True,
        check: bool = False,
    ) -> None:
        """
        Clean this case.

        :param script: If True, use an (All)clean script if it exists. If False, ignore any clean scripts.
        :param check: If True, raise a CalledProcessError if the clean script returns a non-zero exit code.
        """
        script_path = self._clean_script() if script else None

        if script_path is not None:
            await self.run([script_path], check=check)
        else:
            for p in self._clean_paths():
                if p.is_dir():
                    await aioshutil.rmtree(p)  # type: ignore [call-arg]
                else:
                    p.unlink()

    async def run(
        self,
        cmd: Optional[Union[Sequence[Union[str, Path]], str, Path]] = None,
        *,
        script: bool = True,
        parallel: Optional[bool] = None,
        cpus: Optional[int] = None,
        check: bool = True,
    ) -> None:
        """
        Run this case, or a specified command in the context of this case.

        :param cmd: The command to run. If None, run the case. If a sequence, the first element is the command and the rest are arguments. If a string, `cmd` is executed in a shell.
        :param script: If True and `cmd` is None, use an (All)run(-parallel) script if it exists for running the case. If False or no run script is found, autodetermine the command(s) needed to run the case.
        :param parallel: If True, run in parallel using MPI. If None, autodetect whether to run in parallel.
        :param cpus: The number of CPUs to reserve for the run. The run will wait until the requested number of CPUs is available. If None, autodetect the number of CPUs to reserve.
        :param check: If True, raise a CalledProcessError if a command returns a non-zero exit code.
        """
        if cmd is not None:
            if cpus is None:
                if parallel:
                    cpus = min(self._nprocessors, 1)
                else:
                    cpus = 1

            if parallel:
                cmd = self._parallel_cmd(cmd)

            async with self._cpus(cpus):
                await run_process_async(
                    cmd,
                    check=check,
                    cwd=self.path,
                )
        else:
            script_path = self._run_script(parallel=parallel) if script else None

            if script_path is not None:
                if cpus is None:
                    if self._nprocessors > 0:
                        cpus = self._nprocessors
                    else:
                        nsubdomains = self._nsubdomains
                        if nsubdomains is not None:
                            cpus = nsubdomains
                        else:
                            cpus = 1

                await self.run([script_path], check=check, cpus=cpus)

            else:
                if not self and (self.path / "0.orig").is_dir():
                    await self.restore_0_dir()

                if (self.path / "system" / "blockMeshDict").is_file():
                    await self.block_mesh()

                if parallel is None:
                    parallel = (
                        self._nprocessors > 0
                        or (self.path / "system" / "decomposeParDict").is_file()
                    )

                if parallel:
                    if (
                        self._nprocessors == 0
                        and (self.path / "system" / "decomposeParDict").is_file()
                    ):
                        await self.decompose_par()

                    if cpus is None:
                        cpus = min(self._nprocessors, 1)
                else:
                    if cpus is None:
                        cpus = 1

                await self.run(
                    [self.application],
                    parallel=parallel,
                    check=check,
                    cpus=cpus,
                )

    async def block_mesh(self, *, check: bool = True) -> None:
        """Run blockMesh on this case."""
        await self.run(["blockMesh"], check=check)

    async def decompose_par(self, *, check: bool = True) -> None:
        """Decompose this case for parallel running."""
        await self.run(["decomposePar"], check=check)

    async def reconstruct_par(self, *, check: bool = True) -> None:
        """Reconstruct this case after parallel running."""
        await self.run(["reconstructPar"], check=check)

    async def restore_0_dir(self) -> None:
        """Restore the 0 directory from the 0.orig directory."""
        await aioshutil.rmtree(self.path / "0", ignore_errors=True)  # type: ignore [call-arg]
        await aioshutil.copytree(self.path / "0.orig", self.path / "0")

    async def copy(self, dest: Union[Path, str]) -> "AsyncFoamCase":
        """
        Make a copy of this case.

        :param dest: The destination path.
        """
        return AsyncFoamCase(await aioshutil.copytree(self.path, dest, symlinks=True))

    async def clone(self, dest: Union[Path, str]) -> "AsyncFoamCase":
        """
        Clone this case (make a clean copy).

        :param dest: The destination path.
        """
        if self._clean_script() is not None:
            copy = await self.copy(dest)
            await copy.clean()
            return copy

        dest = Path(dest)

        await aioshutil.copytree(
            self.path, dest, symlinks=True, ignore=self._clone_ignore()
        )

        return AsyncFoamCase(dest)
